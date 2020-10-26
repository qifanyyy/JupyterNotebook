import numpy as np
import pandas as pd
import genetic_algorithm_feature_selection.genetic_steps as gs
import genetic_algorithm_feature_selection.variable_selection as vs
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt

nCols = 20
data, target, coefs = make_regression(n_samples=1000,
                                      n_features=nCols,
                                      n_informative=3,
                                      noise=1,
                                      effective_rank=10,
                                      coef=True,
                                      random_state=243)
colnames = np.array([f'X{n}' for n in range(nCols)])
data = pd.DataFrame(data, columns=colnames)
target = pd.Series(target, name='target')
coefs = pd.Series(coefs, index=colnames).sort_values(ascending=False)

#
# calcule performance théorique
# model = LinearRegression()
# population = pd.DataFrame(coefs != 0).T
# res_eval = gs.evaluation_p(population, population.columns,
#                            data, target, model, 'bic')
# score = res_eval.score.values
# print(f"meilleure performance possible : {score}")
#
# model = LinearRegression()
# lst_param = {'lasso_init': False,
#              'n_individus_pop': 20,
#              'n_generations': 60,
#              'n_warming': 2,
#              'pr_croisement': 0.8,
#              'pr_mutation_car': 0.1,
#              'n_cvfolds': 5,
#              'diversification': True,
#              'verbose': 1}
# res_algo_genetique = vs.genetic_algorithm(data, target, model, **lst_param)

n_individus_pop = 10
population = gs.create_population(n_individus_pop,
                                  colnames)

# pop_mutation = gs.mutation(population,
#                            proba_mutation_indiv=0.8,
#                            proba_mutation_car=0.1,
#                            proba_expression=[0.1, 0.9])
#
model = LinearRegression()
pop_mutation = gs.evaluation_p(population, population.columns,
                               data, target, model, 'bic')

pop_selection = gs.selection_i(pop_mutation)
#
# pop_diversifiee = gs.diversification_p(pop_mutation, False)
