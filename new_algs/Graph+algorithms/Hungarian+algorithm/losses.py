from typing import Optional, Callable, Dict

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

# from .HA.hungarian_algorithm import hungarian_algorithm as HA
from scipy.optimize import linear_sum_assignment as HA

from scipy.spatial.distance import cdist

from . import suboptimal_HA as SHA


class TVLoss(nn.Module):
    """
    Total variation функция потерь. Нужна для сглаживания изображения
    и удаления артефактов.
    """
    def __init__(self, weight=1):
        super().__init__()
        self.weight = weight

    def forward(self, x):
        h_tv = F.mse_loss(x[:, :, 1:, :], x[:, :, :-1, :])
        w_tv = F.mse_loss(x[:, :, :, 1:], x[:, :, :, :-1])
        return self.weight * (h_tv + w_tv)


class HungarianLoss(nn.Module):
    """
    Функция потерь для стиля, основанная на венгерском алгоритме.
    """

    def __init__(self, use_suboptimal: bool, hungarian_algorithm: Callable = HA,
                 kmeans_kwargs: Optional[Dict] = None) -> None:
        """
        Инициализация функции потерь.

        Parameters
        ----------
        use_suboptimal : bool
            Использовать ли субоптимальную версию венгерского алгоритма. True,
            если использовать, и False иначе.
        hungarian_algorithm : callable, optional
            Реализация венгерского алгоритма.
        kmeans_kwargs : dict, optional
            Именованные аргументы, которые будут переданы в субоптимальный
            венгреский алгоритм. Подробнее о формате смотрите описание функции
            clusterization_HA в модуле suboptimal_HA.
        """
        super().__init__()
        self.hungarian_algorithm = hungarian_algorithm
        self.use_suboptimal = use_suboptimal
        self.kmeans_kwargs = kmeans_kwargs

    def build_cost_matrix(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        """
        Строит матрицу стоимостей для двух групп точек.

        Parameters
        ----------
        X : np.ndarray
            Первая группа точек.
        Y : np.ndarray
            Вторая группа точек.

        Returns
        -------
        np.ndarray
            Матрицу весов для точек.
        """
        return cdist(X, Y)  # metric у cdist -- можно сделать параметром

    def forward(self, input, target):
        """Размеры входящих тензоров имеют размеры вида (1, C, H, W)"""
        c = input.shape[1]
        X = input.view(c, -1).T   # (h_input * w_input, c)
        Y = target.view(c, -1).T  # (h_target * w_target, c)

        prepare_numpy = lambda x: x.detach().cpu().numpy()
        X_numpy = prepare_numpy(X)
        Y_numpy = prepare_numpy(Y)

        if self.use_suboptimal:
            idx, idy = SHA.clusterization_HA(X_numpy, Y_numpy, self.hungarian_algorithm,
                                             kmeans_kwargs=self.kmeans_kwargs)
        else:
            cost_matrix = self.build_cost_matrix(X_numpy, Y_numpy)
            idx, idy = self.hungarian_algorithm(cost_matrix)

        return nn.MSELoss(reduction='mean')(X[idx], Y[idy])


class GramMatrix(nn.Module):
    """
    Класс для расчета матрицы Грама.
    """
    def forward(self, input):
        b, c, h, w = input.shape
        F = input.view(b, c, h * w)
        G = torch.bmm(F, F.transpose(1, 2))
        G.div_(h * w)
        return G


class GatysLoss(nn.Module):
    """
    Функция потерь для стиля, основанная на матрицах Грама.
    Предложена Леоном Гатисом.
    """
    def __init__(self):
        super().__init__()
        self.gram_matrix = GramMatrix()

    def forward(self, input, target):
        return F.mse_loss(self.gram_matrix(input), self.gram_matrix(target), reduction='mean')


class LinearLossNaive(nn.Module):
    """
    Функция потерь для стиля, основанная на линейном ядре.
    Наивная реализация (требует много ресурсов).
    """
    def forward(self, input, target):
        c = input.shape[1]

        F = input.view(c, -1).T   # (h * w) x c
        S = target.view(c, -1).T  # (h * w) x c

        loss = (F @ F.T).sum() + (S @ S.T).sum() - 2 * (F @ S.T).sum()
        return loss / c ** 2


class LinearLoss(nn.Module):
    """
    Функция потерь для стиля, основанная на линейном ядре.
    Эффективная реализация.
    """
    def forward(self, input, target):
        c = input.shape[1]

        F = input.view(c, -1)   # c x (h_input * w_input)
        S = target.view(c, -1)  # c x (h_target * w_target)

        loss = (F.mean(1) - S.mean(1)).pow(2).sum()
        return loss


class PolynomialLossNaive(nn.Module):
    """
    Функция потерь для стиля, основанная на полиномиальном ядре.
    Наивная реализация (требует много ресурсов).
    """
    def __init__(self, c=0, d=2):
        super().__init__()
        self.c = c
        self.d = d

    def compute_kernel(self, A, B):
        return (A @ B.T + self.c).pow(self.d)

    def forward(self, input, target):
        c = input.shape[1]
        hw_input = input.shape[2] * input.shape[3]
        hw_target = target.shape[2] * target.shape[3]

        F = input.view(c, -1).T   # (h * w) x c
        S = target.view(c, -1).T  # (h * w) x c

        loss = self.compute_kernel(F, F) + self.compute_kernel(S, S) - 2 * self.compute_kernel(F, S)
        return loss.sum() / hw_input / hw_target / c ** 2


class PolynomialLossStochastic(nn.Module):
    """
    Функция потерь для стиля, основанная на полиномиальном ядре.
    Наивная стохастическая реализация (использует несмещенную оценку).
    """
    def __init__(self, c=0, d=2):
        super().__init__()
        self.c = c
        self.d = d

    def compute_kernel(self, A, B):
        """
        Здесь мы считаем несмещенную оценку по M_l = h * w сэмплам. На вход
        принимаются матрица A и B размеров M_l x N_l (N_l = c), и я считаю,
        что в этих матрицах в столбцах с одинаковыми номерами находятся
        соответствующие элементы для подсчета MMD.
        """
        scalar_product = (A * B).sum(dim=1)  # shape = (h * w,)
        kernel_res = (scalar_product + self.c).pow(self.d)
        return kernel_res.mean()

    def forward(self, input, target):
        c = input.shape[1]
        hw_input = input.shape[2] * input.shape[3]
        hw_target = target.shape[2] * target.shape[3]

        F = input.view(c, -1).T   # (h_input * w_input) x c
        S = target.view(c, -1).T  # (h_target * w_target) x c

        num_samples = int((hw_input * hw_target) ** 0.5)  # среднее геометрическое
        num_samples = int(num_samples ** (5 / 4))  # берем больше точек

        i_plus_i_prime = np.random.choice(hw_input, 2 * num_samples)
        i, i_prime = i_plus_i_prime[:num_samples], i_plus_i_prime[num_samples:]
        j_plus_j_prime = np.random.choice(hw_target, 2 * num_samples)
        j, j_prime = j_plus_j_prime[:num_samples], j_plus_j_prime[num_samples:]

        loss = (
            self.compute_kernel(F[i], F[i_prime]) +
            self.compute_kernel(S[j], S[j_prime]) -
            self.compute_kernel(F[i], S[j_prime]) -
            self.compute_kernel(S[j], F[i_prime])
        )

        return loss / c ** 2


class PolynomialLoss(nn.Module):
    """
    Функция потерь для стиля, основанная на полиномиальном ядре.
    Эффективная реализация для случая, когда степень полинома равна 2.
    """
    def __init__(self, c=0, d=2):
        super().__init__()
        if d != 2:
            raise ValueError('Пока что поддерживается только d = 2')
        self.c = c
        self.d = d

    def forward(self, input, target):
        c = input.shape[1]
        hw_input = input.shape[2] * input.shape[3]
        hw_target = target.shape[2] * target.shape[3]

        F = input.view(c, -1)   # c x (h * w)
        S = target.view(c, -1)  # c x (h * w)

        GramF = F @ F.T / hw_input
        GramS = S @ S.T / hw_target
        gram_loss = nn.functional.mse_loss(GramF, GramS, reduction='mean')

        F = F.sum(dim=1)
        S = S.sum(dim=1)
        linear_loss = F.pow(2).sum() + S.pow(2).sum() - 2 * (F * S).sum()
        linear_loss = 2 * self.c * linear_loss / hw_input / hw_target / c ** 2

        loss = gram_loss + linear_loss
        return loss


class GaussianLoss(nn.Module):
    """
    Функция потерь для стиля, основанная на гауссовом ядре.
    Наивная стохастическая реализация (использует несмещенную оценку).

    DEPRECATED! Работает не очень стабильно. Как я понял, так было
    и в изначальной статье.
    """
    def __init__(self, sigma=None):
        super().__init__()
        raise DeprecationWarning('Этот лосс нельзя использовать')

        if sigma is None:
            self.recompute_sigma = True
        else:
            self.recompute_sigma = False
            self.sigma_sq = sigma ** 2

    def compute_kernel(self, A, B):
        """
        Здесь мы считаем несмещенную оценку по M_l = h * w сэмплам. На вход
        принимаются матрица A и B размеров M_l x N_l (N_l = c), и я считаю,
        что в этих матрицах в строках с одинаковыми номерами находятся
        соответствующие элементы для подсчета MMD.
        """
        dists = ((A - B) ** 2).sum(dim=1)
        return torch.exp(-dists / 2 / self.sigma_sq)

    def forward(self, input, target):
        c = input.shape[1]
        hw_input = input.shape[2] * input.shape[3]
        hw_target = target.shape[2] * target.shape[3]

        sample_size = int((hw_input * hw_target) ** 0.5)

        F = input.view(c, -1).T   # (h * w) x c
        S = target.view(c, -1).T  # (h * w) x c

        F_idx = np.random.choice(np.arange(hw_input), size=sample_size)
        S_idx = np.random.choice(np.arange(hw_target), size=sample_size)

        if self.recompute_sigma:
            self.sigma_sq = ((F[F_idx] - S[S_idx]) ** 2).sum(dim=1).mean()

        loss = (hw_input * hw_target / sample_size) * (
            self.compute_kernel(F[F_idx], F[S_idx]) +
            self.compute_kernel(S[F_idx], S[S_idx]) +
            -2 * self.compute_kernel(F[F_idx], S[S_idx])
        ).sum()

        return loss


class BNLoss(nn.Module):
    """
    Функция потерь для стиля, основанная на батч-норм ядре.
    Эффективная реализация.
    """
    def forward(self, input, target):
        c = input.shape[1]

        F = input.view(c, -1)
        S = target.view(c, -1)

        means = (F.mean(dim=1) - S.mean(dim=1)).pow(2)
        stds = (F.std(dim=1) - S.std(dim=1)).pow(2)
        loss = (means + stds).mean()
        
        return loss
