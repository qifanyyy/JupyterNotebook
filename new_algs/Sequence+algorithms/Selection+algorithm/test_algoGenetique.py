import numpy as np
import pandas as pd
import genetic_algorithm_feature_selection.variable_selection as vs
import genetic_algorithm_feature_selection.genetic_steps as gs
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
# import matplotlib.pyplot as plt

nCols = 50
nGoods = 10
data, target, coefs = make_regression(n_samples=1000,
                                      n_features=nCols,
                                      n_informative=nGoods,
                                      noise=1,
                                      effective_rank=10,
                                      coef=True,
                                      random_state=243)
colnames = np.array([f'X{n}' for n in range(nCols)])
data = pd.DataFrame(data, columns=colnames)
target = pd.Series(target, name='target')
coefs = pd.Series(coefs, index=colnames).sort_values(ascending=False)
print(coefs.head(5))

# duplication de colonnes pour voir
# comment se passe la sélection avec algo genetique
data_dup = data.loc[:, coefs[coefs!=0].index] + 2*np.random.randn(1000, nGoods)
data_dup.columns = data_dup.columns + "_dup"

data = pd.concat((data, data_dup), axis=1, sort=False)
nCols = data.shape[1]
colnames = np.array(data.columns)

# calcule performance théorique
model = LinearRegression()
population = pd.DataFrame(coefs != 0).T
res_eval = gs.evaluation_p(population, population.columns,
                           data, target, model, 'bic')
score = res_eval.score.values
print(f"meilleure performance possible : {score}")

# recherche meilleure combinaison de variables
model = LinearRegression()
lst_param = {'lasso_init': False,
             'taille_pop': 5,
             'n_generations': 30,
             'n_warming': 2,  # 5
             'pr_croisement': 0.8,
             'pr_mutation_car': 0.1,
             'n_cvfolds': 5,
             'diversification': True,
             'verbose': 1}
res_algo_genetique = vs.genetic_algorithm(data, target, model, **lst_param)
