import numpy as np
import pandas as pd
import genetic_algorithm_feature_selection.variable_selection as vs
import genetic_algorithm_feature_selection.genetic_steps as gs
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
# from sklearn.datasets import load_boston

# objectif : reproduire les graphiques de Julie Hamon dans sa thèse
# . évolution du meilleur score
# . distribution/boîte moustache des meilleurs scores finaux.

# dataBoston = load_boston()
# featNames =dataBoston['feature_names']
# data = pd.DataFrame(dataBoston['data'], columns=featNames)
# target = pd.Series(dataBoston['target'], name='target')
# RM, LSTAT, INDUS, CRIM, TAX, PTRATIO
# colnames = featNames.copy()

nCols = 500  # 300
data, target, coefs = make_regression(n_samples=1000,
                                      n_features=nCols,
                                      n_informative=10,  # 30
                                      noise=1,
                                      effective_rank=10,
                                      coef=True,
                                      random_state=243)
colnames = np.array([f'X{n}' for n in range(nCols)])
data = pd.DataFrame(data, columns=colnames)
target = pd.Series(target, name='target')
coefs = pd.Series(coefs, index=colnames).sort_values(ascending=False)
print(coefs.head(5))

# calcule performance théorique
model = LinearRegression()
population = pd.DataFrame(coefs != 0).T
res_eval = gs.evaluation_p(population, population.columns,
                           data, target, model, 'bic')
score = res_eval.score.values
print(f"meilleure performance possible : {score}")

# lancement de tests comparatifs
param_to_test = [False, True]
n_tests = 5
results_perf = {}
score_history = {}
# boucle sur les paramètres
for param in param_to_test:
    print(f'\nLance boucle pour paramètre : {param}')
    parname = f'lasso_init_{param}'
    lst_param = {'lasso_init': param,
                 'taille_pop': 20,
                 'n_generations': 50,
                 'n_warming': 5,
                 'pr_croisement': 0.8,
                 'pr_mutation_car': 0.1,
                 'n_cvfolds': 5,
                 'diversification': True,
                 'verbose': 1}
    tmp_res = []
    # refait n_test fois la sélection des variables
    for i in range(n_tests):
        model = LinearRegression()
        res_algo_genetique = vs.genetic_algorithm(data, target,
                                                  model,
                                                  **lst_param)
        # enregistre les résultats
        keyname = (parname, f'run_{i}')
        score_history[keyname] = res_algo_genetique['best_score_history'].values
        tmp_res.append(res_algo_genetique['best_score'])
    results_perf[parname] = np.array(tmp_res)

results_perf = pd.DataFrame(results_perf)
results_history = pd.DataFrame(score_history)

# affiche répartition des scores
results_perf.plot(kind='box', title='Score minimization performance')
plt.show()

# affiche historique des scores
listMainCols = results_history.columns.levels[0]

rose = (1.0, 0.42745098039215684, 0.7137254901960784, 1)
bleuvert = (0.0, 0.5725490196078431, 0.5725490196078431, 1)
orangec = (0.8588235294117647, 0.8196078431372549, 0.0, 1)
lst_colors = [rose, bleuvert, orangec]
subPlots = []
for i, mainCol in enumerate(listMainCols):
    aPlot = plt.plot(results_history.xs(mainCol, axis=1), color=lst_colors[i])
    subPlots.append(aPlot[0])
plt.legend(subPlots, listMainCols)
plt.title('Évolution des performances\nen fonction de la génération')
plt.show()
