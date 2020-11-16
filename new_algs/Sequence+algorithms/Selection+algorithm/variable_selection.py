import numpy as np
import pandas as pd
import genetic_algorithm_feature_selection.genetic_steps as gs
import matplotlib.pyplot as plt
from typing import Any


def genetic_algorithm(data: pd.DataFrame, target: pd.Series,
                      model: Any,
                      lasso_init: bool = True,
                      taille_pop: int = 30,
                      n_generations: int = 100,
                      n_warming: int = 2,
                      pr_croisement: float = 0.8,
                      pr_mutation_car: float = 0.1,
                      n_cvfolds: int = 5,
                      diversification: np.bool = True,
                      verbose: int = 0) -> dict:
    """
    Recherche une combinaison de variables qui approche la performance maximale
    globale. La recherche est faite par un algorithme génétique comportant
    les étapes suivantes à chaque génération :
    création d'une population de parents,
    évaluation des parents,
    croisement puis mutation des enfants,
    mixage des populations de parents et d'enfants.

    :param data: données contenant les observation faites sur les variables
    parmi lesquelles chercher les meilleures
    :param target: variable de sortie pour chaque donnée d'observation
    :param model: modèle à appliquer. Il doit être valide avec les standards
    de scikit-slearn
    :param lasso_init: si True, présélection des variables avec régression Lasso
    pour 50% des individus avant initialisation de la population.
    :param taille_pop: nombre d'individus dans la population.
    :param n_generations: nombre de génération à réaliser, supérieur à 1
    :param n_warming: nombre de générations d'initialisation de la recherche
    de caractères les plus exprimés.
    :param pr_croisement: seuil de probabilité de croisement
    permettant à deux individus de se reproduire
    :param pr_mutation_car: seuil de probabilité de mutation des caractères
    :param n_cvfolds: nombre de plis pour validation croisée du modèle,
    doit être au moins 2
    :param diversification: applique diversification si True
    :param verbose: niveau de retour lors des calculs permet d'afficher
    des informations supplémentaires lors de la recherche - [0 (défaut),1,2]
    :return:
    Un dictionnaire est retourné contenant :
    la liste des meilleures variables à conserver,
    le score obtenu
    """
    print("Démarrage de l'aglorithme génétique")
    # paramètres de l'optimisation
    n_generations = max((2, n_generations))
    n_cvfolds = max((2, n_cvfolds))
    if n_warming > n_generations:
        print("n_warming>n_generation -> fixe n_warning=0")
        n_warming = 0
    if verbose not in [0, 1, 2]:
        print("verbose doit être compris dans [0, 1, 2] -> fixe verbose = 0")
        verbose = 0
    # paramètres globaux
    # taux de sélection des parents
    rt_keep_parents = 0.5
    # score de performance
    score_performance = 'bic'
    # initialisation des individus aléatoirement
    colnames = data.columns
    if lasso_init:
        proba_caracteres = gs.estimate_best_caracteres(data, target)
    else:
        proba_caracteres = None
    population = gs.create_population(taille_pop,
                                      colnames,
                                      proba_caracteres)
    population = gs.remove_twins_p(population, taille_pop)

    best_score_gen = []
    mean_score_gen = []
    n_gen_without_improve = 5
    for gen in range(n_generations):
        debut_gen = (gen % 5 == 0) & (gen != 0)
        if debut_gen | (gen == 1) | (gen == n_generations-1):
            if verbose != 0:
                mean_score_tmp = mean_score_gen[-1]
                max_score_tmp = np.array(best_score_gen)[:, -1].max()
                print(f"itération {gen}",
                      f" - score moyen = {np.round(mean_score_tmp, 2)}",
                      f" - score max = {np.round(max_score_tmp, 2)}")
            if verbose == 2:
                # affichage de la population
                plt.pcolormesh(1*population.values, cmap='Greys')
                plt.xticks(np.arange(population.shape[1])+0.5,
                           colnames, rotation=45, ha='center')
                plt.colorbar()
                plt.show()
        # évaluation des individus
        rang_indiv = gs.evaluation_p(population, colnames, data, target,
                                     model, scorer=score_performance,
                                     n_cv=n_cvfolds,
                                     sort_scores=True)
        # enregistre scores
        max_score = rang_indiv.score.max()
        best_individu = rang_indiv[rang_indiv.score == max_score]
        best_individu = best_individu.values[0].tolist()
        best_score_gen.append(best_individu)
        mean_score_gen.append(rang_indiv.score.mean())

        # calcul taux de variation de meilleure performance
        # sur dernières générations
        tx_var_score = -1
        if gen > n_gen_without_improve+1:
            roll_back_index = range(gen - n_gen_without_improve, gen)
            last_best_score = [best_score_gen[n][-1] for n in roll_back_index]
            tx_var_score = np.mean(last_best_score) / last_best_score[-1]

        # diversification si pas de changement du score max sur 5 itérations
        # ajouter contrainte pour ne pas enchaîner les diversifications
        if diversification & (tx_var_score == 1):
            if verbose > 0:
                print('diversification de la population')
            population = gs.diversification_p(rang_indiv)
        else:
            # sélection des individus
            indiv_pass = gs.selection_i(rang_indiv,
                                        indiv_ratio_to_keep=rt_keep_parents)

            # reproduction : croisement des individus
            # sélection aléatoire de paires de parents parmi tous les possibles
            # nb_childs = int((1-rt_keep_parents) * taille_pop)
            # print(f"après selection indiv_pass {indiv_pass.score.head()}")
            child_population = gs.reproduction(indiv_pass, colnames,
                                               taille_pop_init=taille_pop,
                                               proba_croisement=pr_croisement)

            # mutation des individus suivant proba de muter
            # et uniformité des expressions des caractères
            child_population = gs.mutation(child_population,
                                           proba_mutation_car=pr_mutation_car,
                                           proba_expression=(0.1, 0.9))

            # evaluation des enfants
            child_population = gs.evaluation_p(child_population, colnames,
                                               data, target,
                                               model, scorer=score_performance,
                                               sort_scores=False)

            # remplacement des individus peu performant
            # conserver meilleurs parmi parents initiaux et
            # enfants issus des meilleurs
            # création de population de taille égale à population initiale
            # indiv_pass peut être ordonné
            # child_population ne doit pas être ordonné
            # print(f"avant mixage taille populations\n",
            #       f"rang_indiv {rang_indiv.shape} -",
            #       f" child_pop {child_population.shape}")
            population = gs.mixage_parents_enfants(rang_indiv, child_population)
            population = population.drop('score', axis=1)

            # remplacement des individus doublons par des individus aléatoires
            # + complétion de la population pour stabiliser nombre d'individus
            population = gs.remove_twins_p(population, taille_pop)

    all_columns = colnames.tolist() + ['score']
    best_score_gen = pd.DataFrame(best_score_gen, columns=all_columns)
    # suppression des générations d'initialisation
    best_score_gen = best_score_gen.loc[n_warming:, :]
    max_best_score = best_score_gen.score.max()
    index_score_max = best_score_gen.score == max_best_score
    best_all_individus = best_score_gen.loc[index_score_max, colnames].iloc[0]
    best_all_individus.name = 'best_individu'

    # affiche nombre de sélection des variables pour les meilleurs individus
    best_individus_unique = best_score_gen.sort_values(by='score',
                                                       ascending=False)
    best_individus_unique = best_individus_unique.drop_duplicates()
    nb_sel_variable = best_individus_unique.sum(axis=0)
    nb_sel_variable = nb_sel_variable.sort_values(ascending=False).drop('score')
    prc_sel_variable = nb_sel_variable/len(best_individus_unique)
    # création du dictionnaire de sortie
    # avec inversion des scores : on veut minimiser les erreurs
    dict_output = {'best_individu': best_individus_unique.iloc[0, :],
                   'best_score': -1*max_best_score,
                   'best_score_history': -1*best_score_gen.score,
                   'importance_variable': prc_sel_variable}

    if verbose == 2:
        dict_output['importance_variable'].plot(kind='bar')
        plt.xlabel('Variables')
        plt.ylabel('Proportion de sélection des variables')
        plt.title('Sélection des variables des meilleurs '
                  'individus à chaque itération')
        plt.tight_layout()
        plt.show()
    return dict_output
