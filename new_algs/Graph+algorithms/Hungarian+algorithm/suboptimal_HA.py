import warnings
from typing import List, Dict, Callable, Optional

import numpy as np

# from .HA.hungarian_algorithm import hungarian_algorithm as HA
from scipy.optimize import linear_sum_assignment as HA
from scipy.optimize import minimize

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

from . import core


# @@@ Субоптимальный алгоритм со случайными сэмплами @@@ #

def split_arr(arr: np.ndarray, num_parts: int = 3) -> List[np.ndarray]:
    """
    Равномерно разделяет массив arr на num_parts частей.

    Parameters
    ----------
    arr : ndarray
        Массив, который нужно разбить на части.
    num_parts
        Количество частей, на которое нужно разбить массив.

    Returns
    -------
    list of ndarrays:
        Список частей исходного разбитого массива.

    Examples
    --------
    >>> x = np.arange(13)
    >>> split_arr(x, 3)
    [array([0, 1, 2, 3]), array([4, 5, 6, 7]), array([ 8,  9, 10, 11, 12])]
    """
    n = arr.size
    base_len = n // num_parts
    num_longer = n % num_parts

    lens = [base_len] * (num_parts - num_longer) + [base_len + 1] * num_longer
    split_idx = np.cumsum(lens)

    return np.split(arr, split_idx[:-1])


def suboptimal_HA(
    cost_matrix : np.ndarray,
    hungarian_algorithm: Callable = HA,
    num_parts: int = 100,
    random_seed: Optional[int] = None
) -> core.IdxIdy:
    """
    Субоптимальная версия венгерского алгоритма со случайным выбором кластеров.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Матрица стоимостей.
    hungarian_algorithm : callable, optional
        Функция, которая по матрице стоимостей решает задачу о назначениях.
        По умолчанию используется реализация из библиотеки scipy.
    num_parts : int, optional
        Количество кластеров, на которые разибваются точки.
        По умолчанию равно 3.
    random_seed : optional
        Случайное зерно для генератора случайных чисел. По умолчанию равен None.

    Returns
    -------
    idx, idy : np.ndarrays
        Индексы соответствующих точек.
    """
    n, m = cost_matrix.shape

    if num_parts == 1:
        return hungarian_algorithm(cost_matrix)

    if random_seed is not None:
        np.random.seed(random_seed)  # для возпроизводимости результатов

    rnd_idx = np.random.permutation(n)
    rnd_idy = np.random.permutation(m)

    rnd_idx_parts = split_arr(rnd_idx, num_parts)
    rnd_idy_parts = split_arr(rnd_idy, num_parts)

    idx, idy = [], []
    for idx_part, idy_part in zip(rnd_idx_parts, rnd_idy_parts):
        cur_cost_matrix = cost_matrix[idx_part][:, idy_part]
        cur_idx, cur_idy = hungarian_algorithm(cur_cost_matrix)
        idx += idx_part[cur_idx].tolist()
        idy += idy_part[cur_idy].tolist()

    return np.array(idx), np.array(idy)


# @@@ Субоптимальный алгоритм с кластеризацией @@@ #

def get_optimal_K(n: int, I: int):
    """
    Подсчитывает оптимальное число кластеров на основании сложности итогового
    алгоритма, выраженной через число кластеров.

    Parameters
    ----------
    n : int
        Число точек в каждой из групп.
    I : int
        Число итераций алгоритма кластеризации K-Means.

    Returns
    -------
    int, tuple of ints
        Оптимальное значение для количества кластеров и итоговые
        сложности алгоритма.
    """
    def C(K: int, split_return: bool = False):
        a = n * K * I
        b = K ** 3
        c = n ** 3 / K ** 2
        if split_return:
            return a + b + c, a, b, c
        return a + b + c

    def C_der(K: int) -> int:
        return 3 * K ** 2 + n * I - 2 * n ** 3 / K ** 3

    res_opt = minimize(C, np.array(100), jac=C_der)
    optK = res_opt.x

    return optK, C(optK, split_return=True)


def equalize_arrays(a: np.ndarray, b: np.ndarray) -> core.IdxIdy:
    """
    Уравнивает массивы по размеру (в большую сторону) путем досэмплирования
    элементов в массив меньшей длины.

    Parameters
    ----------
    a : np.ndarray
        Первый массив.
    b : np.ndarray
        Второй массив.

    Returns
    -------
    np.ndarray, np.ndarray
        Уравненные массивы.
    """
    def equalize(a: np.ndarray, b: np.ndarray) -> core.IdxIdy:
        """
        Уравнивает массивы по размеру с учетом, что массив a короче массива b.

        Parameters
        ----------
        a : np.ndarray
            Первый массив.
        b : np.ndarray
            Второй массив.

        Returns
        -------
        np.ndarray, np.ndarray
            Уравненные массивы.
        """
        if len(a) >= len(b):
            raise ValueError('a должен быть короче')
        num_to_sample = len(b) - len(a)
        a = np.r_[a, np.random.choice(a, num_to_sample)]
        return a, b

    if len(a) < len(b):
        a, b = equalize(a, b)
    elif len(a) > len(b):
        b, a = equalize(b, a)
    return a, b


def clusterization_HA(
    opt_matrix: np.ndarray,
    target_matrix: np.ndarray,
    HA: Callable,
    verbose: int = 0,
    kmeans_kwargs: Optional[Dict] = None
) -> core.IdxIdy:
    """
    Субоптимальная версия венгерского алгоритма с кластеризацией.

    Parameters
    ----------
    opt_matrix : np.ndarray
        Матрица размера N x D с точками, которые нужно сопоставить с точками из
        матрицы target_matrix.
    target_matrix : np.ndarray
        Матрица размера M x D с точками, которые нужно сопоставить с точками из
        матрицы opt_matrix.
    HA : callable
        Реализация венгерского алгоритма.
    verbose : int, optional
        Сила логирования работы функции. Нужна в первую очередь для функции
        кластеризации kmeans. По умолчанию равен 0.
    kmeans_kwargs : dict, optional
        Именованные аргументы, которые будут переданы в функцию
        кластеризации kmeans. Ожидаются параметры init, max_iter и n_clusters.

        Параметр init отвечает за инициализацию kmeans. Может быть равен 'random'
        или 'k-means++'. По умолчанию выставится 'random'.

        Параметр max_iter отвечает за число итераций алгоритма кластеризации.
        По умполчанию выставится 50.

        В качестве параметра n_clusters может быть передан коллбэк, который по
        числу точек для кластеризации и числу итераций алгоритма кластеризации
        выдает количество кластеров. Также в качестве параметра n_clusters
        может быть передан tuple из коллбэка и его письменного описания
        (описание будет проигнорировано). Также n_clusters может быть равен
        'auto', в этом случае будет считаться оптимальное с точки зрения
        быстродействия количество кластеров.
        По умолчанию будет считаться оптимальное с точки зрения быстродействия
        количество кластеров.
    Returns
    -------
    idx, idy : np.ndarrays
        Индексы сопоставленных точек.
    """

    # Обрабатываем аргументы функции.
    kmeans_kwargs = kmeans_kwargs.copy()
    if kmeans_kwargs is None:
        kmeans_kwargs = {}
    if 'init' not in kmeans_kwargs:
        kmeans_kwargs['init'] = 'random'  # 'random' или 'k-means++'
        warnings.warn('Инициализация kmeans не была задана, поэтому она была выставлена в "random"')
    if 'max_iter' not in kmeans_kwargs:
        kmeans_kwargs['max_iter'] = 50
        warnings.warn('Количество итераций kmeans не было задано, поэтому оно было выставлено в 50')
    if 'n_clusters' not in kmeans_kwargs:
        kmeans_kwargs['n_clusters'] = 'auto'
        warnings.warn('Количество кластеров kmeans не было задано, поэтому оно будет выбираться оптимальным образом')

    n_clusters = kmeans_kwargs['n_clusters']
    if isinstance(n_clusters, int):
        n_clusters_callback = lambda *args: n_clusters
    elif isinstance(n_clusters, str):
        if n_clusters == 'auto':
            n_clusters_callback = lambda *args: get_optimal_K(*args)[0]
        else:
            raise ValueError('Если n_clusters -- строка, то оно должно быть равно "auto"')
    elif isinstance(n_clusters, tuple):
        n_clusters_callback = n_clusters[0]  # n_clusters[1] -- это письменное описание функции
    else:
        n_clusters_callback = n_clusters

    # Определяем вспомогательную функцию.
    def prepare_matrix(matrix: np.ndarray):
        """
        Функция для создания кластеризатора для точек одной из групп точек, его
        обучения и подсчета представителей кластеров.

        Parameters
        ----------
        matrix : np.ndarray
            Точки одной из групп точек.

        Returns
        -------
        clust : sklearn kmeans clusterization function
            Кластеризатор точек.
        clust_labels : np.ndarray
            Метки кластеров для всех точек.
        embeds : np.ndarray
            Представители (эмбеддинги) кластеров.
        embed_id2label : np.ndarray
            Перевод индексов представителей в метку кластера.
        """
        # K_opt = max(1, n // 10)
        kmeans_kwargs['n_clusters'] = n_clusters_callback(matrix.shape[0], kmeans_kwargs['max_iter'])

        clust = KMeans(n_init=1, **kmeans_kwargs, verbose=verbose)  # precompute_distances=True
        clust_labels = clust.fit_predict(matrix)
        embed_id2label = np.unique(clust_labels)
        num_clusters = embed_id2label.shape[0]

        embeds = np.empty((num_clusters, matrix.shape[1]), dtype=matrix.dtype)
        for cluster_id, cluster_num in enumerate(embed_id2label):
            cur_clust_mask = (clust_labels == cluster_num)
            embeds[cluster_id] = matrix[cur_clust_mask].mean(axis=0)

        return clust, clust_labels, embeds, embed_id2label

    # Кластеризуем обе группы точек.
    opt_clust, opt_clusters, opt_embeds, opt_embed_id2label = prepare_matrix(opt_matrix)
    target_clust, target_clusters, target_embeds, target_embed_id2label = prepare_matrix(target_matrix)

    ### Считаем примерную сложность рассчетов
    # n = opt_matrix.shape[0]
    # K_opt = get_optimal_K(n, I)
    # counts = np.bincount(opt_clusters)
    # total_C = K_opt[0] ** 3 + np.sum(counts ** 3)
    # print(C(1, n, I) / total_C)

    # Сопоставляем кластера из двух групп между собой.
    cluster_idx = np.arange(opt_embeds.shape[0])
    cluster_idy = np.arange(target_embeds.shape[0])
    cluster_idx, cluster_idy = equalize_arrays(cluster_idx, cluster_idy)
    opt_embed_id2label_fixed = opt_embed_id2label[cluster_idx]
    target_embed_id2label_fixed = target_embed_id2label[cluster_idy]

    cluster_cost_matrix = euclidean_distances(opt_embeds[cluster_idx], target_embeds[cluster_idy])
    cluster_idx, cluster_idy = HA(cluster_cost_matrix)
    # cluster_idx и cluster_idy -- это сопоставление кластеров для оптимизируемой картинки и стиля

    # Производим сопоставление точек внутри сопоставленных кластеров.
    suboptimal_idx, suboptimal_idy = [], []
    for opt_embed_id, target_embed_id in zip(cluster_idx, cluster_idy):
        opt_clust_num = opt_embed_id2label_fixed[opt_embed_id]
        target_clust_num = target_embed_id2label_fixed[target_embed_id]

        opt_mask = opt_clusters == opt_clust_num
        X = opt_matrix[opt_mask]

        target_mask = target_clusters == target_clust_num
        Y = target_matrix[target_mask]

        cur_idx = np.arange(X.shape[0])
        cur_idy = np.arange(Y.shape[0])
        cur_idx, cur_idy = equalize_arrays(cur_idx, cur_idy)
        trans_idx = np.arange(X.shape[0])[cur_idx]
        trans_idy = np.arange(Y.shape[0])[cur_idy]

        XY_cost_matrix = euclidean_distances(X[cur_idx], Y[cur_idy])

        cur_idx, cur_idy = HA(XY_cost_matrix)
        cur_idx = trans_idx[cur_idx]
        cur_idy = trans_idy[cur_idy]

        opt_ind = np.where(opt_mask)[0]
        suboptimal_idx += opt_ind[cur_idx].tolist()

        target_ind = np.where(target_mask)[0]
        suboptimal_idy += target_ind[cur_idy].tolist()

    return np.array(suboptimal_idx), np.array(suboptimal_idy)
