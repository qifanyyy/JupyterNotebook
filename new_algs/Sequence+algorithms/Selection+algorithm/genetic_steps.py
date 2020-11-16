import numpy as np
import pandas as pd
from itertools import combinations
from sklearn.linear_model import LassoCV
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import make_scorer, SCORERS
from typing import Any, Tuple
TDfloat = Tuple[float, float]

# TODO global : voir si modification d'ordre des noms des colonnes

def get_bic(y_true: np.array, y_pred: np.array, k: int = 10) -> float:
    """
    Calcul critère d'information bayesien (BIC)
    :param y_true: valeur cible à prédire (numpy.array)
    :param y_pred: valeur prédite pour y_true (numpy.array)
    :param k:nombre de variables du modèle (int)
    :return:
    bic: critère d'information bayesien (float)
    """
    sse = sum((y_true-y_pred)**2)
    n = len(y_true)
    bic = n*np.log(sse/n) + k*np.log(n)
    return bic


def min_max_scaler(dfvalues: pd.Series,
                   lower_bound: float = 0,
                   upper_bound: float = 1,
                   invert_low_up: np.bool = False) -> pd.Series:
    """
    Mise à l'échelle d'une Series pandas entre borne inférieure et supérieure
    :param dfvalues: séries pandas à mettre à l'échelle (pandas.Series)
    :param lower_bound: borne inférieure
    :param upper_bound: borne supérieure
    :param invert_low_up: déclenche l'inversion des bornes min et max
    :return:
    scaledValues: séries mise à l'échelle (pandas.Series)
    """
    if dfvalues.var() != 0:
        min_dfvalues = dfvalues.min()
        max_dfvalues = dfvalues.max()
        dfvalues_std = (dfvalues - min_dfvalues) / (max_dfvalues - min_dfvalues)
        scaledvalues = (dfvalues_std * (upper_bound-lower_bound) + lower_bound)
    else:
        scaledvalues = pd.Series(np.zeros(len(dfvalues)))
    scaledvalues = 1-scaledvalues if invert_low_up else scaledvalues
    return scaledvalues


def get_nb_jumeaux(population: np.array, taille_pop_init: int) -> dict:
    """
    Calcul nombre d'individus jumeaux dans population
    et nombre d'individus à ajouter si on supprime l'un des jumeaux
    :param population: liste des individus à traiter (numpy.array)
    :param taille_pop_init: nombre d'individus de la population initiale (int)
    :return:
    nb_to_add: nombre d'individus à ajouter
    """
    pop_individus_unique = np.unique(population, axis=0)
    nb_indiv_unique = len(pop_individus_unique)
    nb_to_add = max(0, taille_pop_init - nb_indiv_unique)
    return {'nb_to_add': nb_to_add,
            'pop_individus_unique': pop_individus_unique}


def estimate_best_caracteres(data: pd.DataFrame,
                             target: pd.Series) -> pd.Series:
    """
    Calcul d'une régression linéaire pénalisée pour estimer les paramètres
    de chacun des caractères.
    Conversion des paramètres ajustés en score entre 0 et 1 pour les utiliser
    comme probabilité de sortie pour l'initialisation de la population
    :param data: observations pour lesquelles la sélection de variable est faite
    :param target: variable à expliquer
    :return:
    proba_caracteres: liste des probabilités associées aux caractères
    """
    fitted = LassoCV(cv=2, max_iter=1000, n_jobs=-1).fit(data, target)
    proba_caracteres = pd.Series(fitted.coef_, index=data.columns)
    # proba minimale de 0.25 de sélection des caractères
    proba_caracteres = min_max_scaler(proba_caracteres,
                                      lower_bound=0.25, upper_bound=0.75,
                                      invert_low_up=False)
    return proba_caracteres


def _random_population(nb_individus: int,
                       nb_caracteres: int) -> np.array:
    """
    Tirage aléatoire de caractères pour créer une population d'individus
    :param nb_individus: nombre d'individus dans la population
    :param nb_caracteres:liste des caractères exprimables par les individus
    :return:
    population: liste des individus constituant la population
    """
    population = np.random.randint(0, 2, nb_individus * nb_caracteres)
    population = population.astype(np.bool)
    return population


def create_population(nb_individus: int,
                      list_caracteres: np.array,
                      proba_caracteres: Any = None) -> pd.DataFrame:
    """
    Création d'une population d'individus présentant
    des caractères aléatoires ou non.
    Si probabilités des caractères fournies,
    alors 50% des individus sont générés en suivant ces probabilité,
    l'autre partie est générée de façon uniforme
    :param nb_individus: nombre d'individus dans la population
    :param list_caracteres: liste des caractères exprimables par les individus
    :param proba_caracteres: probabilité d'expression des caractères si pas None
    :return:
    population: liste des individus de la population
    """
    nb_caracteres = len(list_caracteres)
    if proba_caracteres is None:
        population = _random_population(nb_individus, nb_caracteres)
    else:
        half_population = int(np.round(nb_individus/2, 0))
        population = _random_population(half_population, nb_caracteres)
        rest_population = nb_individus - half_population
        for i in range(rest_population):
            proba_individu = np.random.random(nb_caracteres)
            individu = proba_individu < proba_caracteres
            population = np.concatenate((population, individu))
    population = population.reshape((nb_individus, nb_caracteres))
    population = pd.DataFrame(population, columns=list_caracteres)
    return population


def evaluation_p(population: pd.DataFrame, list_caracteres: np.array,
                 data: pd.DataFrame, target: pd.Series,
                 model: Any, scorer: str,
                 n_cv: int = 5,
                 sort_scores: bool = True) -> pd.DataFrame:
    """
    Évaluation des individus d'une population
    :param population: ensemble des individus à évaluer
    :param list_caracteres: liste des caractères qui peuvent être exprimés
    :param data: données à utiliser pour l'évaluation
    :param target: sortie à prédire
    :param model: modèle à ajuster
    :param scorer: score de performance à maximiser
    :param n_cv: nombre de plis pour validation croisée, doit être au moins de 2
    :param sort_scores: appliquer un tri (descendant) ou non
    :return:
    population avec score de performance obtenu par validation croisée
    """
    # TODO: voir pour passer directement la fonction scorer=make_score()
    #  et les paramètres associés pour ne pas la définir en dur
    population_eval = population.copy()
    mean_scores = []
    xval_strategy = KFold(n_cv, shuffle=True, random_state=123)
    for indiv in population_eval.values:
        lstcols = list_caracteres[indiv]
        if scorer in SCORERS.keys():
            scoring_function = scorer
        elif scorer == 'bic':
            kwargs = {'k': len(lstcols)}
            scoring_function = make_scorer(get_bic,
                                           greater_is_better=False,
                                           **kwargs)
        else:
            print(f'Scorer {scorer} unknown')
            break
        scores = cross_val_score(model, data[lstcols], target,
                                 cv=xval_strategy,
                                 scoring=scoring_function,
                                 n_jobs=-1)
        mean_scores.append(scores.mean())
    population_scores = pd.Series(mean_scores,
                                  index=population_eval.index,
                                  name='score')
    population_eval['score'] = population_scores
    if sort_scores:
        population_eval = population_eval.sort_values(by='score',
                                                      ascending=False)
    else:
        population_eval = population_eval.reset_index(drop=True)
    return population_eval


def selection_i(population_df: pd.DataFrame,
                keep_indiv_above_mean_score: bool = False,
                indiv_ratio_to_keep: float = 0.5,
                population_size: int = None) -> pd.DataFrame:
    """
    Sélection des meilleurs individus si keep_indiv_above_mean_score est True
    parmi une population triée par score décroissant.
    Sinon conserve un certain pourcentage d'individus de la population initiale
    par la méthode de tournoi.
    :param population_df: population des individus triés par score
    de performance décroissant
    :param indiv_ratio_to_keep: pourcentage des individus à conserver
    :param keep_indiv_above_mean_score: garder individus meilleurs
    que la moyenne
    :param population_size: taille de la population,
    si None (defaut), utilise population courante pour calculer la taille
    :return:
    population_kept: liste des individus conservés avec leur score
    """
    # TODO : ajouter sélection par tournoi :
    #  prendre 3 individus et garder le meilleur
    #  jusqu'à en avoir le nombre voulu
    population_kept = population_df.copy()
    nb_individus = population_kept.shape[0]
    if keep_indiv_above_mean_score and (nb_individus > 1):
        std_score = population_kept.score.std()
        mean_score = population_kept.score.mean() if std_score != 0 else -9e6
        indiv_better_score = population_kept.score > mean_score
        if indiv_better_score.sum() > 1:
            return population_kept.loc[population_kept.score > mean_score, :]
        else:
            return population_kept.iloc[:2, :]
    elif nb_individus > 1:
        if population_size is None:
            population_size = nb_individus
        nb_indiv_to_keep = int(indiv_ratio_to_keep * population_size)
        # garde le meilleur individu
        idx_to_keep = [population_kept.score.idxmax()]
        # sélection par tournoi parmi 3 individus issus des individus restants
        for k in range(nb_indiv_to_keep-1):
            available_idx = population_kept.index.difference(idx_to_keep)
            # vérifie que population assez grande pour sélectionner 3 individus
            if len(available_idx) >= 3:
                idx_fight = np.random.choice(available_idx, 3,
                                             replace=False)
                idx_winner = population_kept.loc[idx_fight, 'score'].idxmax()
                idx_to_keep.append(idx_winner)
        population_kept = population_kept.loc[idx_to_keep, :]
        population_kept = population_kept.reset_index(drop=True)
        return population_kept
    else:
        print("Nombre d'individus insuffisant\n-->Population périclite")


def croise_parents_pivot(parent1: pd.Series,
                         parent2: pd.Series) -> list:
    population_enfant = []
    nb_caracteres = len(parent1)
    pos_pivot = np.random.randint(0, nb_caracteres)
    enfant1 = parent1[:pos_pivot] + parent2[pos_pivot:]
    enfant2 = parent2[:pos_pivot] + parent1[pos_pivot:]
    population_enfant.append([np.bool(car) for car in enfant1])
    population_enfant.append([np.bool(car) for car in enfant2])
    return population_enfant


def croise_parents_ssocf(parent1: pd.Series,
                         parent2: pd.Series) -> dict:
    """
    calcul croisement de 2 parents par la méthode SSOCF [Emmanouilidis 2000]
    voir pages 102-103 dans thèse de julie hamon
    :param parent1: pandas.Series
    :param parent2: pandas.Series
    :return:
    :population: numpy.array
    """
    # parent1 = pd.Series([1, 0, 1, 1, 0, 0, 1, 1, 1])
    # parent2 = pd.Series([0, 1, 1, 0, 0, 1, 0, 1, 0])
    parent1 = parent1.astype(int)
    parent2 = parent2.astype(int)
    # list_caracteres = parent1.index.tolist()
    nb_caract_expr_parent1 = np.sum(parent1)
    nb_caract_expr_parent2 = np.sum(parent2)
    caract_communs = np.equal(parent1, parent2)
    cumul_caract_expr = (1 * parent1.values + 1 * parent2.values)
    nb_caract_expr_communs = np.sum(cumul_caract_expr > 1)
    # nb_caract_communs = caract_communs.sum()
    nb_caract_non_communs_expr = np.maximum(1, np.invert(caract_communs).sum())
    diff_caract_expr_p1 = nb_caract_expr_parent1 - nb_caract_expr_communs
    diff_caract_expr_p2 = nb_caract_expr_parent2 - nb_caract_expr_communs
    pe1 = diff_caract_expr_p1 / nb_caract_non_communs_expr
    pe2 = diff_caract_expr_p2 / nb_caract_non_communs_expr
    pe = [pe1, pe2]
    indiv = [parent1, parent2]
    # 2 parents = 2 enfants
    # calcul proba d'héritage des caractères
    population_enfant = []
    proba_herit_from_parent = []
    for i_enfant in range(2):
        enfant = []
        proba_herit_from_parent.append(1-pe[i_enfant])
        for c, caract_is_commun in enumerate(caract_communs):
            proba_heritage = np.random.rand()
            if caract_is_commun:
                # enfant garde caractère
                # TODO : parfois KEYError:0 à cette ligne. voir Pourquoi !!
                enfant.append(indiv[i_enfant][c])
            # caractère non commun et proba héritage OK
            elif proba_heritage <= pe[i_enfant]:
                # caractère hérité du parent
                enfant.append(indiv[i_enfant][c])
            else:
                # caractère hérité du parent
                enfant.append(not indiv[i_enfant][c])
        enfant = [np.bool(car) for car in enfant]
        population_enfant.append(enfant)
    # print(f"ssocf proba_herit_from_parent {proba_herit_from_parent}")
    population_enfant = {'population_enfant': population_enfant,
                         'proba_heritage': proba_herit_from_parent}
    return population_enfant


def reproduction(list_parents: pd.DataFrame,
                 list_caracteres: np.array,
                 taille_pop_init: int,
                 proba_croisement: float = 0.8) -> pd.DataFrame:
    """
    Reproduction des parents qui donnent 2 enfants. Calcule probabilité
    de reproduction à partir des scores de performance.
    Reproduction jusqu'à avoir autant d'enfants
    que la taille de la population initiale
    Score dans population enfant est issue du produit des scores des parents
    et de la proba d'héritage, normalisé entre 0 et 1.
    :param list_parents: liste des parents
    :param list_caracteres: liste des caractères
    :param taille_pop_init: taille de la population initiale
    :param proba_croisement: probabilité de croisement seuil
    :return:
    liste des enfants et score
    """
    use_ssocf = True
    nb_parents = list_parents.shape[0]
    if nb_parents > 1:
        # calcul proba de croisement des paires de parents
        # à partir du produit des performances
        parents_df = list_parents.copy()
        # passer valeurs entre 0 et 1 avec inversion de l'ordre
        # pour utiliser comme proba de croisement
        parents_df['score'] = min_max_scaler(parents_df['score'],
                                             lower_bound=0,
                                             upper_bound=1,
                                             invert_low_up=True)
        # print(f"reproduction parent_scores {parents_df['score'].head()}")
        paires_parents = np.array(list(combinations(parents_df.index, 2)))
        paires_parents = np.random.permutation(paires_parents)
        scores_crossed = np.array([])
        for i in range(len(paires_parents)):
            sc1 = parents_df.loc[paires_parents[i, 0], 'score']
            sc2 = parents_df.loc[paires_parents[i, 1], 'score']
            sc = sc1 * sc2
            scores_crossed = np.append(scores_crossed, sc)
        # print(f"reproduction score_crossed {scores_crossed}")
        cpt_enfants = 0
        population_enfant = []
        scores_crossed_enfants = []
        for j, (ipar1, ipar2) in enumerate(paires_parents):
            proba_pairs = scores_crossed[j]
            if (len(paires_parents) == 1) | \
                ((proba_pairs <= proba_croisement) &
                 (cpt_enfants < taille_pop_init)):
                cpt_enfants += 2
                parent1 = parents_df.loc[ipar1, list_caracteres]
                parent2 = parents_df.loc[ipar2, list_caracteres]
                # pas de croisement si parents identiques
                if (parent1 == parent2).all():
                    cpt_enfants -= 2
                    continue
                elif use_ssocf:
                    """ croisement par méthode SSOCF """
                    # print(f"avant ssocf parent1 et parent2",
                    #       f"\n{parent1}\n{parent2}")
                    enfants_heritage = croise_parents_ssocf(parent1, parent2)
                    enfants = enfants_heritage['population_enfant']
                    proba_heritage = enfants_heritage['proba_heritage']
                    sc_enfant1 = proba_pairs*proba_heritage[0]
                    sc_enfant2 = proba_pairs*proba_heritage[1]
                else:
                    """ croisement avec un pivot """
                    enfants = croise_parents_pivot(parent1, parent2)
                    sc_enfant1, sc_enfant2 = proba_pairs, proba_pairs
                population_enfant.append(enfants)
                scores_crossed_enfants.append(sc_enfant1)
                scores_crossed_enfants.append(sc_enfant2)
        population_enfant = np.array(population_enfant)
        if population_enfant.shape != (0,):
            dim_pop_enfant = population_enfant.shape
            new_nb_lines = dim_pop_enfant[0]*dim_pop_enfant[1]
            nb_cols = dim_pop_enfant[2]
            population_enfant = population_enfant.reshape(new_nb_lines, nb_cols)
            population_enfant = pd.DataFrame(population_enfant,
                                             columns=list_caracteres)
            # inverser ordre scores pour retrouver problème de maximisation
            scores_crossed_enfants = pd.Series(scores_crossed_enfants)
            # print(f"reproduction scores {scores_crossed_enfants.head()}")
            population_enfant['score'] = min_max_scaler(scores_crossed_enfants,
                                                        invert_low_up=True)
        else:
            population_enfant = pd.DataFrame(list_parents.iloc[0]).T
            population_enfant['score'] = 1
            print("parents identiques")
            # TODO : pose problème :Traceback (most recent call last):
            #   File "/media/jmehault/winDocuments/MesProjets/AlgoGenetique/test_algoGenetique.py", line 52, in <module>
            #     res_algo_genetique = vs.genetic_algorithm(data, target, model, **lst_param)
            #   File "/media/jmehault/winDocuments/MesProjets/AlgoGenetique/src_genetic_algo/variable_selection.py", line 162, in genetic_algorithm
            #     population = gs.remove_twins_p(population, taille_pop)
            #   File "/media/jmehault/winDocuments/MesProjets/AlgoGenetique/src_genetic_algo/genetic_steps.py", line 508, in remove_twins_p
            #     population_unique = get_nb_jumeaux(pop_wo_twins, taille_pop_init)
            #   File "/media/jmehault/winDocuments/MesProjets/AlgoGenetique/src_genetic_algo/genetic_steps.py", line 60, in get_nb_jumeaux
            #     pop_individus_unique = np.unique(population, axis=0)
            #   File "/usr/lib64/python3.7/site-packages/numpy/lib/arraysetops.py", line 254, in unique
            #     raise TypeError(msg.format(dt=ar.dtype))
            # TypeError: The axis argument to unique is not supported for dtype object
        # print(f"fin reproduction population_enfant",
        #       f"{population_enfant.score.head()}")
        return population_enfant
    else:
        print('Nombre de parents < 2 : reproduction impossible')


def mutation(population: pd.DataFrame,
             proba_mutation_car: float = 0.1,
             proba_expression: TDfloat = (0.1, 0.9)) -> pd.DataFrame:
    """
    Mutation des individus d'une population, pour un seul caractère
    en fonction de leur rang de performance.
    La probabilité de muter d'individu est p = (n/nmax)**2, avec n son rang
    et nmax la taille de la population à muter).
    Si aucun caractère n'est sélectionné, mutation de 1 ou 2 aléatoirement.
    Si l'expression des caractères est trop uniforme, alors ce caractère mute.
    :param population: liste des individus de la population à muter
    :param proba_mutation_car: seuil de probabilité de mutation des caractères
    :param proba_expression: seuils min et max d'expression des caractères
    pour limiter l'uniformisation des individus de la population
    :return:
    mute_population: population avec mutations (pandas;DataFrame)
    """
    mute_population = population.copy()
    rang_indiv = mute_population.score.rank(ascending=False)
    mute_population = mute_population.drop('score', axis=1)
    mute_population = mute_population.values
    nb_individus, nb_caracteres = np.shape(mute_population)
    proba_mute_indiv = (rang_indiv / nb_individus) ** 2
    for i, indiv in enumerate(mute_population):
        # test proba de mutation
        proba_mute = np.random.rand()
        if proba_mute <= proba_mute_indiv[i]:
            proba_mute_car = np.random.rand(nb_caracteres)
            caractere_mute = np.argwhere(proba_mute_car <= proba_mutation_car)
            caractere_mute = caractere_mute.flatten()
            individu_mute = indiv.copy()
            individu_mute[caractere_mute] = ~(individu_mute[caractere_mute])
            mute_population[i] = individu_mute
        # si aucun caractère sélectionné
        # force un ou deux caractères à être exprimés
        if np.sum(mute_population[i]) == 0:
            caractere_mute = np.random.randint(0, nb_caracteres, 2)
            mute_population[i][caractere_mute[0]] = True
            mute_population[i][caractere_mute[1]] = True
    # vérifie que caractères exprimés non uniformes
    # pour chaque caractère uniforme, mute son expression de p% des individus
    proba_expression_obs = mute_population.sum(axis=0) / nb_individus
    expression_faible = np.argwhere(proba_expression_obs <= proba_expression[0])
    expression_faible = expression_faible.flatten()
    possible_indiv = range(nb_individus)
    proba_mute_indiv = proba_mute_indiv/sum(proba_mute_indiv)
    n_indiv_redesse = max(1, int(0.05*nb_individus))
    for caractere in expression_faible:
        individu_mute = np.random.choice(possible_indiv, n_indiv_redesse,
                                         replace=False, p=proba_mute_indiv)
        mute_population[individu_mute, caractere] = True
    expression_forte = np.argwhere(proba_expression_obs >= proba_expression[1])
    expression_forte = expression_forte.flatten()
    for caractere in expression_forte:
        individu_mute = np.random.choice(possible_indiv, n_indiv_redesse,
                                         replace=False, p=proba_mute_indiv)
        mute_population[individu_mute, caractere] = False
    list_caracteres = population.columns.difference(['score'], sort=False)
    mute_population = pd.DataFrame(mute_population,
                                   columns=list_caracteres,
                                   index=population.index)
    return mute_population


def mixage_parents_enfants(parents_df: pd.DataFrame,
                           enfants_df: pd.DataFrame) -> pd.DataFrame:
    """
    Mixage des parents et enfant par comparaison des enfants
    avec moins bon parent présent. Si enfant meilleur que parent,
    parent supprimé sinon enfant supprimé. La nouvelle population est
    la concaténation des individus restant.
    :param parents_df: liste des parents avec score
    :param enfants_df: liste des enfants avec score
    :return:
    mixage_pop: liste mixée
    """
    list_parents = parents_df.copy()
    list_enfants = enfants_df.copy()
    nb_enfants = len(list_enfants)
    for cpt_indiv in range(nb_enfants):
        index_worst_parent = list_parents.score.idxmin()
        current_child = list_enfants.xs(cpt_indiv, axis=0)
        if current_child['score'] > list_parents.score.min():
            list_parents = list_parents.drop(index_worst_parent, axis=0)
        else:
            list_enfants = list_enfants.drop(cpt_indiv, axis=0)
    mixage_pop = pd.concat((list_parents, list_enfants),
                           axis=0, sort=False, ignore_index=True)
    return mixage_pop


def remove_twins_p(population: pd.DataFrame,
                   taille_pop_init: int) -> pd.DataFrame:
    """
    Suppression des individus jumeaux, complète population si besoin
    Termine par permutation des individus
    :param population: ensemble des individus (pandas.DataFrame)
    :param taille_pop_init: taille de la population initiale à conserver (int)
    :return:
    population sans jumeaux
    """
    pop_wo_twins = population.copy()
    if 'score' in pop_wo_twins.columns:
        pop_wo_twins = pop_wo_twins.drop('score', axis=1)
    list_caracteres = pop_wo_twins.columns.difference(['score'], sort=False)
    pop_wo_twins = pop_wo_twins.values
    population_unique = get_nb_jumeaux(pop_wo_twins, taille_pop_init)
    nb_to_add = population_unique['nb_to_add']
    pop_wo_twins = population_unique['pop_individus_unique']
    while nb_to_add != 0:
        individus_to_add = create_population(nb_to_add, list_caracteres)
        pop_wo_twins = np.concatenate((pop_wo_twins,
                                       individus_to_add), axis=0)
        population_unique = get_nb_jumeaux(pop_wo_twins,
                                           taille_pop_init)
        nb_to_add = population_unique['nb_to_add']
        pop_wo_twins = population_unique['pop_individus_unique']
    pop_wo_twins = np.random.permutation(pop_wo_twins)
    pop_wo_twins = pd.DataFrame(pop_wo_twins,
                                columns=list_caracteres,
                                dtype=np.bool)
    return pop_wo_twins


def diversification_p(population_df: pd.DataFrame,
                      full_alea: np.bool = False) -> pd.DataFrame:
    """
    Diversification de la population
    si full_alea = False:
    On garde les individus de l'ancienne population dont score > moyenne
    On complète la population avec des individus issus des meilleurs
    dont on altère les caractères vus dans chacun d'eux par tirage uniforme
    si full_area = True: remplace toute la population par distribution uniforme
    :param population_df: population avec score de performance
    :param full_alea: diversification des meilleurs individus par défaut,
    sinon diversification de toute la population
    :return:
    population après diversification
    """
    # TODO : ajouter paramètre sur % des individus conservés intacts
    #  pour éviter création de nombreux individus avec score très proche
    #  => modifier fonction selection_p
    # TODO : intégrer notion d'historique prc_sel_variable
    #  dans la diversification pour inverser les probabilités
    #  d'expression des caractères ?
    list_caracteres = population_df.columns.difference(['score'], sort=False)
    nb_caracteres = len(list_caracteres)
    population_score_sort = population_df.sort_values(by='score',
                                                      ascending=False)
    alter_population = selection_i(population_score_sort,
                                   keep_indiv_above_mean_score=True)
    alter_population = alter_population.drop('score', axis=1)
    index_alter_population = alter_population.index.values
    nb_indiv_alter = len(alter_population)
    nb_individus = len(population_df) - nb_indiv_alter
    if full_alea:
        new_individus = create_population(nb_individus, list_caracteres)
        population = pd.concat((alter_population, new_individus),
                               axis=0, sort=True)
    else:
        # diversification des meilleurs individus
        # sélection des caractères sur/sous représentés par rapport à uniforme
        ratio_sel_caracteres = alter_population.sum() / len(alter_population)
        shift_ratio_car = ratio_sel_caracteres-0.5
        extrem_exp_car = shift_ratio_car[abs(shift_ratio_car) > 0.25]
        caract_to_change = extrem_exp_car.index.tolist()
        population = np.array([], dtype=np.bool)
        nb_repetitions = int(nb_individus / len(index_alter_population)) + 1
        # liste des meilleurs individus
        roll_indiv_index = np.tile(index_alter_population,
                                   nb_repetitions)[:nb_individus]
        # boucle sur les individus à muter
        for indiv_idx in roll_indiv_index:
            individu = alter_population.loc[indiv_idx, list_caracteres]
            # impose expression si caractère trop uniforme
            car_to_false = extrem_exp_car[extrem_exp_car > 0].index
            individu[car_to_false] = np.random.choice([True, False],
                                                      p=[0.25, 0.75])
            car_to_true = extrem_exp_car[extrem_exp_car < 0].index
            individu[car_to_true] = np.random.choice([True, False],
                                                     p=[0.75, 0.25])
            # les autres caractères sont tirés aléatoirement
            idx_caract_alea = ~individu.index.isin(car_to_false | car_to_true)
            caract_alea = individu[idx_caract_alea].index
            create_divers = np.random.randint(0, 2, len(caract_alea))
            create_divers = create_divers.astype(np.bool)
            individu[caract_alea] = create_divers
            while individu.sum() == 0:
                # tire aléatoirement un caractère à modifier
                caractere_mute = np.random.choice(caract_to_change)
                individu.at[caractere_mute] = np.bool(1)
            population = np.append(population, individu.values)
        population = population.reshape((nb_individus, nb_caracteres))
        # remplace dernier individu de alter_population par individu
        # avec les caractères les plus exprimés (>95%) dans alter_population
        select_all_alter_but_last = alter_population.values[:-1, :]
        population = np.concatenate((select_all_alter_but_last, population),
                                    axis=0)
        prc_exp_car = alter_population.sum(axis=0)/nb_indiv_alter
        # TODO : quel facteur appliquer pour sélection les caractères exprimé ?
        car_most_expr = (prc_exp_car > prc_exp_car.max() * 0.90).values
        # vérifie que au moins un caractère dépasse le seuil de 95% d'expression
        check_exp_car = car_most_expr.any()
        if check_exp_car:
            car_most_expr = car_most_expr.reshape(1, nb_caracteres)
        else:
            # si aucun ne passe le seuil
            # on récupère le dernier individu de alter_population
            car_most_expr = alter_population.values[-1, :]
            car_most_expr = car_most_expr.reshape(1, nb_caracteres)
        population = np.concatenate((population, car_most_expr), axis=0)
        idx_population = range(population.shape[0])
        population = pd.DataFrame(population,
                                  columns=list_caracteres,
                                  index=idx_population,
                                  dtype=np.bool)
    return population
