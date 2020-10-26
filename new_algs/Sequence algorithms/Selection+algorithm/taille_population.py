import time
import numpy as np
import pandas as pd
import genetic_algorithm_feature_selection.variable_selection as vs
import genetic_algorithm_feature_selection.genetic_steps as gs
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.feature_selection import RFECV
from mlxtend.feature_selection import SequentialFeatureSelector
# import matplotlib.pyplot as plt
resDict = {}

listNCols = [100, 500, 1000, 2500]
listRatioGoods = [0.1, 0.25, 0.5, 0.75]
for nCols in listNCols:
    for ratioGood in listRatioGoods:
        nGoods = int(nCols * ratioGood)
        print(f"Nb colonnes : {nCols}, nb goods : {nGoods}")
        nEch = 1000
        data, target, coefs = make_regression(n_samples=nEch,
                                              n_features=nCols,
                                              n_informative=nGoods,
                                              noise=1,
                                              effective_rank=10,
                                              coef=True,
                                              random_state=243)
        colnames = np.array([f"X{n}" for n in range(nCols)])
        data = pd.DataFrame(data, columns=colnames)
        target = pd.Series(target, name='target')
        coefs = pd.Series(coefs, index=colnames)
        coefs = coefs.sort_values(ascending=False)
        print(coefs.head(5))

        # duplication de colonnes pour voir
        # comment se passe la sélection avec algo genetique
        data_dup = data.loc[:, coefs[coefs!=0].index]
        data_dup = data_dup + 2*np.random.randn(nEch, nGoods)
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

        listRatioPop = [0.05, 0.1, 0.15, 0.2, 0.25]
        listRatioGen = [0.3, 0.5 ,0.6]
        couplesFait = []
        for ratioPop in listRatioPop:
            for ratioGen in listRatioGen:
                taillePop = max(30, int(ratioPop * nCols))
                nGen = int(ratioGen * nCols)
                coupleAFaire = (taillePop, nGen)
                if coupleAFaire in couplesFait:
                    print(f"Couple {coupleAFaire} déjà fait")
                    continue
                else:
                    couplesFait.append((taillePop, nGen))
                    print(f"Taille population : {taillePop}, "
                          f"nb generations : {nGen}")
                    # recherche meilleure combinaison de variables
                    model = LinearRegression()
                    print(f"Démarre sélection par génétique")
                    timeStart = time.time()
                    lst_param = {'lasso_init': False,
                                'taille_pop': taillePop,
                                'n_generations': nGen,
                                'n_warming': 2,  # 5
                                'pr_croisement': 0.8,
                                'pr_mutation_car': 0.1,
                                'n_cvfolds': 5,
                                'diversification': True,
                                'verbose': 0}
                    res_algo_genetique = vs.genetic_algorithm(data, target,
                                                              model,
                                                              **lst_param)
                    dureeGenetique = time.time() - timeStart
                    scoreGenetique = res_algo_genetique['best_score']

                    resDict[(nCols, nGoods, taillePop, nGen)] = {'duree': dureeGenetique,
                                                                'score': scoreGenetique}

# tracer temps d'execution, meilleure performance pour chaque méthode,
# nombre de variables conservées
# en fonction du nombre total de variables et du rapport nbVarVraies/nbVarTot

resDf = pd.DataFrame(resDict).T
resDf.index.names = ['nCols', 'nGood', 'selAlgo']
resDf.to_csv("Etude_population_vs_donnees.csv", sep=';')
# graphiques:
## temps d'exécution pour (nCols,nGood)
## score pour (nCols,nGood)
## meilleur algo de sélection pour score pour (nCols,nGood)
## meilleur algo de sélection pour temps d'exécution pour (nCols,nGood)
