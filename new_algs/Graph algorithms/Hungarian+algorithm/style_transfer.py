import time
import warnings
from argparse import Namespace
from typing import Optional, Union, List, Tuple

import torch
import torch.nn as nn
from torch import optim

from . import core
from . import VGG
from . import losses
from . import image_utils as IU


def gatys_style_loss_weight_callback(depth: int) -> float:
    """
    Коллбэк для стилевых весов для стилизации алгоритмом Гатиса. В алгоритме
    Гатиса веса рассчитываются по формуле 10^3 / (depth^2), где depth --
    глубина слоя (то есть количество каналов в нем).

    Parameters
    ----------
    depth : int
        Количество каналов в слое, на котором считается стилевая функция
        потерь.

    Returns
    -------
    weight : float
        Вес перед стилевой функцией потерь для данного слоя.
    """
    return 1e3 / depth ** 2


def linear_style_loss_weight_callback(depth: int) -> float:
    """
    Коллбэк для стилевых весов для стилизации с помощью линейного ядра.
    Эмпирически были подобраны следующие веса: 2 * 10^7 / (depth^2),
    где depth -- глубина слоя (то есть количество каналов в нем).

    Parameters
    ----------
    depth : int
        Количество каналов в слое, на котором считается стилевая функция
        потерь.

    Returns
    -------
    weight : float
        Вес перед стилевой функцией потерь для данного слоя.
    """
    return 2e7 / depth ** 2


def polynomial_style_loss_weight_callback(depth: int) -> float:
    """
    Коллбэк для стилевых весов для стилизации с помощью полиномиального ядра.
    Эмпирически были подобраны следующие веса: 10^3 / (depth^2),
    где depth -- глубина слоя (то есть количество каналов в нем).

    Parameters
    ----------
    depth : int
        Количество каналов в слое, на котором считается стилевая функция
        потерь.

    Returns
    -------
    weight : float
        Вес перед стилевой функцией потерь для данного слоя.
    """
    return 1e3 / depth ** 2


def BN_style_loss_weight_callback(depth: int) -> float:
    """
    Коллбэк для стилевых весов для стилизации с помощью батч-норм ядра.
    Эмпирически были подобраны следующие веса: 10^7 / (depth^2),
    где depth -- глубина слоя (то есть количество каналов в нем).

    Parameters
    ----------
    depth : int
        Количество каналов в слое, на котором считается стилевая функция
        потерь.

    Returns
    -------
    weight : float
        Вес перед стилевой функцией потерь для данного слоя.
    """
    return 1e7 / depth ** 2


def hungarian_style_loss_weight_callback(depth: int) -> float:
    """
    Коллбэк для стилевых весов для стилизации венгерским алгоритмом. В
    венгерском алгоритме веса перед всеми стилевыми функциями потерь равны 1.

    Parameters
    ----------
    depth : int
        Количество каналов в слое, на котором считается стилевая функция
        потерь. В данном коллбэке этот параметр не используется.

    Returns
    -------
    weight : float
        Вес перед стилевой функций потерь для данного слоя. В данном случае
        равен 1.
    """
    return 1.0


def process_layers(layers, all_layers: Union[List[str], Tuple[str]]) -> List[str]:
    """
    Обрабатывает названия слоев, на которых будут считаться функции потерь.
    Благодаря этой функции можно кратко описывать названия нужных слоев.
    Вместо 'r41', например, можно писать только цифру '4'.

    Parameters
    ----------
    layers : None or str or iterable of layers' names
        Названия слоев, на которых считаются функции потерь.
        layers может быть:
        1. None. В таком случае список будет пустым, то есть потери для
            данных слоев будут равны 0.
        2. 'all'. В таком случае в качестве слоев берутся все слои из списка
            all_layers.
        3. 'no'. В таком случае список слоев будет также пустым (как и в
            пункте 1).
        4. Iterable. Тогда в случае, если это iterable со строками (str),
            то считается, что все объекты в layers -- полные названия слоев.
            Если же это iterable не строк, то считается, что его элементы --
            это номера слоев, на которых нужно считать функции потерь. То есть,
            в частности, layers может быть равна, например, строке '34', тогда
            на выходе получится список ['r31', 'r41'].
    all_layers : list of str or tuple of str
        Список всех слоев, на которых обычно считаются функции потерь. Он будет
        использоваться в случае, когда layers является строкой 'all'. Во всех
        остальных случаях он игнорируется.
        В случае стилевых функций потерь он равен ['r11', 'r21', 'r31', 'r41',
        'r51'], а в случае контентных функций потерь он равен ['r42'].

    Returns
    -------
    layers : list of str
        Список с полными названиями слоев, на которых будут считаться функции
        потерь.
    """
    if layers is None:
        layers = []
    elif isinstance(layers, str):
        if layers == 'all':
            layers = all_layers
        elif layers == 'no':
            layers = []
        else:
            layers = [f'r{layer}{all_layers[0][-1]}' for layer in layers]
    else:
        layers = [layer if isinstance(layer, str) else f'r{layer}{all_layers[0][-1]}' for layer in layers]
    return layers


def make_losses_weigths_targets(
    style_image: torch.Tensor,
    content_image: torch.Tensor,
    style_layers='all',
    content_layers='all',
    style_loss_class=losses.GatysLoss,
    content_loss_class=nn.MSELoss,
    style_loss_weight_callback=None,
    use_always_optimal_for_45: bool = True,
    vgg=None,
    **style_loss_kwargs
) -> Tuple[Namespace, Namespace]:
    """
    Определение слоев, на которых считаются функции потерь, самих функций
    потерь, весов для функций потерь и целевых тензоров для переноса стиля.

    Parameters
    ----------
    style_image : torch.Tensor
        Стилевое изображение, сконвертированное в torch.Tensor, готовое к
        подаче в VGG-16.
    content_image : torch.Tensor
        Контентное изображение, сконвертированное в torch.Tensor, готовое к
        подаче в VGG-16.
    style_layers : None or str or iterable of layers' names, optional
        Задает названия слоев, на которых будут считаться стилевые функции
        потерь. Сначала style_layers будут обработаны с помощью функции
        process_layers. По умолчанию используются все стандартные слои.
    content_layers : None or str or iterable of layers' names, optional
        Задает названия слоев, на которых будут считаться контентные функции
        потерь. Сначала content_layers будут обработаны с помощью функции
        process_layers. По умолчанию используются все стандартные слои.
    style_loss_class : loss class or list of loss classes, optional
        Либо класс для стилевых функций потерь, либо список классов для
        стилевых функций потерь (вместо класса может быть передан инстанс
        класса функции потерь, тогда параметр **style_loss_kwargs будет
        проигнорирован). В первом случае будет использован один класс
        для всех стилевых слоев, во втором случае для каждого стилевого слоя
        будет использоваться соответствующий класс из списка. По умолчанию
        используется losses.GatysLoss.
    content_loss_class : loss class, optional
        Класс для контентных функций потерь (вместо класса может быть передан
        инстанс класса функции потерь). По умолчанию используется nn.MSELoss.
    style_loss_weight_callback : function or str or None, optional
        Коллбэк для определения весов для слоев.
        Если имеет тип str, то может быть:
        1. 'gatys'. В этом случае будет использован
            gatys_style_loss_weight_callback.
        2. 'hungarian'. В этом случае будет использован
            hungarian_style_loss_weight_callback.
        3. 'auto'. В этом случае будет использована автоматическая настрока
            весов.
        Если равен None, то будет использован gatys_style_loss_weight_callback,
        при этом будет выдан warning об этом. Предполагается, что пользователь
        должен явно задать, какой коллбэк ему нужен.
        По умолчанию style_loss_weight_callback равен None.
    use_always_optimal_for_45 : bool, optional
        Использовать ли для самых глубоких (4-5) слоев всегда оптимальные
        алгоритмы. Имеет смысл, только когда среди style_layers есть функция
        потерь, основанная на венгерском алгоритме (losses.HungarianLoss).
        По умолчанию равно True.
    vgg : optional
        Инстанс vgg. Если None, то будет создан новый инстанс VGG.
        По умполчанию None.
    **style_loss_kwargs
        Именованные аргументы, которые будут переданы в классы для стилевых
        функций потерь. Игнорируются для переданных инстансов стилевых функций
        потерь.

    Returns
    -------
    style_params : Namespace
        Параметры для стилевых функций потерь.
        Namespace с полями loss_layers, loss_fns, loss_weights и targets:
        1. loss_layers : list of str
            Слои, на которых будут считаться стилевые функции потерь.
        2. loss_fns : list of callable
            Стилевые функции потерь.
        3. loss_weights : None or list of float
            Веса для стилевых функций потерь.
        4. targets : list of torch.Tensor
            Целевые тензоры, по которым рассчитываются стилевые функции потерь.
    content_params : Namespace
        Параметры для контентной функции потерь.
        Namespace с полями loss_layer, loss_fn, loss_weight и target:
        1. loss_layer : str
            Слой, на котором будет считаться контентная функция потерь.
        2. loss_fn : callable
            Контентная функция потерь.
        3. loss_weight : float
            Веса для контентной функции потерь.
        4. target : torch.Tensor
            Целевой тензор, по которому рассчитывается контентная функция
            потерь.
    """

    # Определение слоев, на которых считаются функции потерь
    if isinstance(style_loss_class, str) and style_loss_class == 'HungarianLoss':
        style_loss_class = losses.HungarianLoss

    if style_loss_weight_callback is None:
        style_loss_weight_callback = gatys_style_loss_weight_callback
        warnings.warn('style_loss_weight_callback не задан и поэтому был выставлен в значение по умолчанию')
    elif isinstance(style_loss_weight_callback, str):
        if style_loss_weight_callback.lower() == 'gatys':
            style_loss_weight_callback = gatys_style_loss_weight_callback
        elif style_loss_weight_callback.lower() in ['ha', 'hungarian']:
            style_loss_weight_callback = hungarian_style_loss_weight_callback
        elif style_loss_weight_callback.lower() == 'auto':
            pass
        else:
            raise ValueError('Если style_loss_weight_callback типа str, то можно задавать '
                             'только гатис лосс, венгерский лосс или автоматическую настройку весов')

    style_params = Namespace(loss_layers=None, loss_fns=None, loss_weights=None, targets=None)
    content_params = Namespace(loss_layer=None, loss_fn=None, loss_weight=None, target=None)

    style_params.loss_layers = process_layers(style_layers, ['r11', 'r21', 'r31', 'r41', 'r51'])
    content_layers = process_layers(content_layers, ['r42'])

    # Определение слоя и веса для контентной функции потерь
    if len(content_layers) == 0:
        # Если контент не нужно накладывать, то создадим фиктивный слой для контента.
        # Он нужен, чтобы работала эквализация
        content_params.loss_layer = 'r42'
        content_params.loss_weight = 0
    else:
        content_params.loss_layer = content_layers[0]
        content_params.loss_weight = 1

    # Определение функций потерь
    if not (isinstance(style_loss_class, list) or isinstance(style_loss_class, tuple)):
        # Если style_loss_class представляет собой класс, а не список классов
        style_loss_class = [style_loss_class] * len(style_params.loss_layers)

    if len(style_loss_class) != len(style_params.loss_layers):
        raise ValueError('Количество слоев и функций потерь не совпадает')

    style_params.loss_fns = []
    for loss_class, layer in zip(style_loss_class, style_params.loss_layers):
        if isinstance(loss_class, nn.Module):
            # Если пришел инстанс класса для стилевой функции потерь, то просто его сохраняем
            style_params.loss_fns.append(loss_class)
        else:
            if (
                loss_class is losses.HungarianLoss and
                style_loss_kwargs['use_suboptimal'] and
                use_always_optimal_for_45 and
                int(layer[1]) >= 4
            ):
                # Используем точный лосс для слоев 4-5 и приближенный для более ранних слоев
                cur_style_loss_kwargs = style_loss_kwargs.copy()
                cur_style_loss_kwargs['use_suboptimal'] = False
            else:
                cur_style_loss_kwargs = style_loss_kwargs
            style_params.loss_fns.append(loss_class(**cur_style_loss_kwargs))
    # print(style.loss_fns)
    if isinstance(content_loss_class, nn.Module):
        # Если пришел инстанс класса для контентной функции потерь, то просто его сохраняем
        content_params.loss_fn = content_loss_class
    else:
        content_params.loss_fn = content_loss_class()

    # Определение весов для стилевых фукнций потерь
    if style_loss_weight_callback == 'auto':
        style_params.loss_weights = None
    else:
        vgg_conv_layers_depth = [64, 128, 256, 512, 512]
        style_layers_depths = [vgg_conv_layers_depth[int(layer[1]) - 1] for layer in style_params.loss_layers]
        style_params.loss_weights = [style_loss_weight_callback(d) for d in style_layers_depths]

    # Определение целевых тензоров для оптимизации
    if vgg is None:
        vgg = VGG.get_vgg_instance()
    with torch.no_grad():
        style_params.targets = vgg(style_image, style_keys=style_params.loss_layers)
        content_params.target = vgg(content_image, content_key=content_params.loss_layer)

    return style_params, content_params


# В LBFGS оно уже зашито DONE:
#   TO DO: добавить определение сходимости (opt_img по норме изменился несильно, на 0.5, например)
def style_transfer(
    opt_img: torch.Tensor,
    style_params: Namespace,
    content_params: Namespace,
    equalize_content_and_style: bool = True,
    stylization_strength: Optional[float] = None,
    wanted_style_losses_contrib='default',
    measure_losses_contribution: bool = False,
    tv_loss_weight: float = 0.0,
    max_iter: int = 500,
    print_iter: Union[int, bool] = 100,
    show_iter: Union[int, bool] = 100,
    history_update_freq: Union[int, bool] = 1,
    return_gif: bool = False,
    verbose: int = 3,
    postprocess_opt_image: bool = True,
    vgg=None
) -> Namespace:
    """
    Процесс переноса стиля.

    Parameters
    ----------
    opt_img : torch.Tensor
        Оптимизируемое изображение (стилизация).
    style_params : Namespace
        Параметры для стилевых функций потерь. Namespace с полями loss_layers,
        loss_fns, loss_weights и targets. Подробнее см. в возвращаемых
        значениях функции make_losses_weigths_targets.
    content_params : Namespace
        Параметры для контентной функции потерь. Namespace с полями loss_layer,
        loss_fn, loss_weight и target: Подробнее см. в возвращаемых значениях
        функции make_losses_weigths_targets.
    equalize_content_and_style : bool
        Нужно ли уравнивать силу наложения стиля и контента. True, если нужно,
        False иначе.
    stylization_strength : float, optional
        Сила наложения стиля. Должна быть задана (не равна None), если нужно
        уравнивать силу наложения стиля и контента (equalize_content_and_style =
        = True).
        По умолчанию None.
    wanted_style_losses_contrib : optional
        Желаемые вклады для отдельных стилевых лоссов. Должно быть похожим на
        массив, а сумма всех элементов должна быть равна единице.
        Предполагается, что придут 5 весов для пяти слоев: с 1 по 5.
        Веса перед стилевыми функциями потерь будут изменены так, что вклады
        отдельных функций потерь станут равными заданным в
        wanted_style_losses_contrib.
        Также может быть равно None, False, True и 'default'. Если равно None
        или False, то перевзвешивание производиться не будет. Если равно True
        или 'default', то используются бейзлайновые вклады, подсчитанные по
        алгоритму стилизации Леона Гатиса.
        По умолчанию равно 'default', то есть используются бейзлайновые вклады.
    measure_losses_contribution : bool, optional
        Нужно ли делать замеры для вкладов слоев в итоговое значение функции
        потерь. True, если надо, False иначе. Это инструмент для того, чтобы
        посчитать бэйзлайновые вклады стилевых лоссов для последующей
        эквализации алгоритмов стилизации. Если замеры делаются, то они
        возвращаются в атрибуте all_MAGs возвращаемого Namespace.
        По умолчанию выключено (False).
    tv_loss_weight : float, optional
        Вес для total variation функции потерь. Total variation функция потерь
        нужна для сглаживания изображения и избавления от артефактов. А
        артефакты появляются как при использовании алгоритма Гатиса, так и при
        использовании венгерского алгоритма.
        По умолчанию не используется (равен 0.0).
    max_iter : int, optional
        Количество итераций для оптимизатора. По умолчанию 500.
    print_iter : int or bool, optional
        Частота вывода на экран информации о процессе оптимизации.
        По умолчанию 100 (то есть раз в 100 итераций информация выводится
        на экран). Также может быть равно False, в этом случае вывод информации
        на экран будет отключен.
    show_iter : int or bool, optional
        Частота вывода на экран оптимизируемого изображения (стилизации).
        По умолчанию 100 (то есть раз в 100 итераций изображение выводится
        на экран). Также может быть равно False, в этом случае вывод изображений
        на экран будет отключен.
    history_update_freq : int or bool, optional
        Частота обновления информации о процессе оптимизации, которая будет
        потом возвращена из функции. По умолчанию 1 (то есть информация
        обновляется на каждой итераций). Также может быть равно False, в этом
        случае сохранение информации будет отключено.
    return_gif : bool, optional
        Сохранять ли оптимизируемое изображение на каждой итерации (например,
        для того, чтобы потом проследить за процессом стилизации в виде
        gif-изображения). True, если надо сохранять, False иначе. Если
        сохранение изображений производится, то они возвращаются в атрибуте
        images возвращаемого Namespace. Иначе в этом атрибуте будет
        значение None.
        По умолчанию сохранение стилизаций отключено (False).
    verbose : int, optional
        Задает силу многословности при выводе дополнительной информации на
        экран. Если 0, то дополнительная информация на экран не выводится.
        Пока что максимальное значение -- 150. По умолчанию равно 3.
    postprocess_opt_image : bool, optional
        Нужно ли приводить итоговую стилизацию (которая является тензором) в
        изображение типа PIL.Image.Image. True, если нужно, False иначе.
        Полезно, если после процесса переноса стиля больше не планируется
        дальнейших переносов стиля с данной стилизацией.
        По умолчанию стилизация приводится к типу PIL.Image.Image
        (значение True).
    vgg : optional
        Инстанс vgg. Если None, то будет создан новый инстанс VGG.
        По умполчанию None.

    Returns
    -------
    Namespace
        Информация о процессе переноса стиля.
        Namespace с полями opt_img, history, images и all_MAGs:
        1. opt_img : PIL.Image.Image or torch.Tensor
            Итоговая стилизация
        2. history : dict from str to list
            Замеры разных величин за время процесса переноса стиля:
            a. n_iter
                Номер итерации, на котором были сделаны измерения.
            b. loss
                Значение итоговой функции потерь, сделанное на данной итерации.
            c. time
                Сколько времени прошло с момента прошлого замера.
        3. images : None or list of PIL.Image.Image
            Стилизации с каждой итерации, если параметр return_gif равен True.
            Иначе None.
        4. all_MAGs : None or list of torch.Tensor
            Замеры вкладов слоев в значение итоговой функцию потерь, если
            measure_losses_contribution равен True. Иначе None.
    """

    # Проверяем аргументы
    if equalize_content_and_style and stylization_strength is None:
        raise ValueError('Сила стилизации должна быть задана при уравнивании стиля и контента')
    if not equalize_content_and_style and stylization_strength is not None:
        raise ValueError('Сила стилизации может быть задана только при уравнивании стиля и контента')
        # Так как о силе стилизации можно говорить только тогда, когда достигнут некоторый баланс
        # между вкладами стиля и контента

    if wanted_style_losses_contrib is None or wanted_style_losses_contrib is False:
        wanted_style_losses_contrib = None
    elif wanted_style_losses_contrib is True or wanted_style_losses_contrib == 'default':
        # TODO: проверка на то, что у нас ровно те слои для стилевых лоссов, что мы ждем
        wanted_style_losses_contrib = torch.tensor([
            1.1238664388656616, 11.46979808807373, 11.010421752929688, 74.66542053222656, 1.7304834127426147
        ], device=core.device) / 100
    elif not isinstance(wanted_style_losses_contrib, torch.Tensor):
        wanted_style_losses_contrib = torch.tensor(wanted_style_losses_contrib, device=core.device)

    if wanted_style_losses_contrib is None and style_params.loss_weights is None:
        raise ValueError('Не выбран автоматический выбор весов для стиля и при этом не заданы веса для стиля')

    if wanted_style_losses_contrib is not None and style_params.loss_weights is not None:
        warnings.warn('Вы используете автоматическую настройку весов для стилевых лоссов, но при этом '
                      'задали свои веса для стилевых лоссов. Веса будут настроены автоматически')

    if style_params.loss_weights is not None and not isinstance(style_params.loss_weights, torch.Tensor):
        style_params.loss_weights = torch.tensor(style_params.loss_weights, device=core.device)

    # if equalize_content_and_style != (wanted_style_losses_contrib is not None):
    #     warnings.warn('Этот режим вроде должен работать, но может быть и нет. На всякий случай предупреждаю')

    # Инициализация логирования и результатов работы функции
    history = {
        'n_iter': [],
        'loss': [],
        'time': [],
        # 'style_weight': [],
    }

    images = None
    if return_gif:
        images = []

    all_MAGs = None
    if measure_losses_contribution:
        all_MAGs = []

    if measure_losses_contribution and verbose >= 100:
        print(style_params.loss_layers, content_params.loss_layer)

    if vgg is None:
        vgg = VGG.get_vgg_instance()

    # Для того, чтобы не считать по нескольку раз все функции потерь
    #  на одной итерации, будем их кэшировать в переменной cur_losses.
    cur_losses = None

    # Определяем функции для обучения
    def calc_losses() -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Считает значения функций потерь для стиля, контента и значение total
        variation функции потерь.

        Returns
        -------
        style_losses : torch.Tensor
            Значения стилевых функций потерь (по одному значению на каждый слой).
        content_loss : torch.Tensor
            Значение контентной функции потерь (одно значение).
        tv_loss : torch.Tensor or float
            Значение total variation функции потерь, если вес для нее
            положительный. Иначе 0 (это небольшая оптимизация, чтобы не считать
            функцию потерь, которая не вносит вклада в итоговоую функцию потерь).
        """
        # optimizer.zero_grad()  # Вроде не нужно, так как обнулять градиенты нужно перед backward.

        nonlocal cur_losses
        if cur_losses is None:
            style_outs, content_out = vgg(opt_img, style_params.loss_layers, content_params.loss_layer)

            style_losses = [
                loss_fn(out, target) for loss_fn, out, target in
                zip(style_params.loss_fns, style_outs, style_params.targets)
            ]
            content_loss = content_params.loss_fn(content_out, content_params.target)
            tv_loss = tv_loss_weight * losses.TVLoss()(opt_img) if tv_loss_weight > 0 else 0

            cur_losses = torch.stack(style_losses), content_loss, tv_loss

        # Делаем копии, чтобы исходные значения функций потерь не перезаписались
        return tuple(loss.clone() for loss in cur_losses)

    def calc_loss() -> torch.Tensor:
        """
        Считает значение итоговой функции потерь.

        Returns
        -------
        loss : torch.Tensor
            Значение итоговой функции потерь (одно число).

        """
        style_losses, content_loss, tv_loss = calc_losses()
        style_loss = torch.sum(style_params.loss_weights * style_losses)
        content_loss *= content_params.loss_weight
        return style_loss + content_loss + tv_loss

    def calc_MAG(loss: torch.Tensor) -> float:
        """
        Для данного значения функции потерь рассчитывает его вклад, то есть MAG
        (mean absolute gradients).

        Parameters
        ----------
        loss : torch.Tensor
            Значение функции потерь.

        Returns
        -------
        MAG : float
            Вклад лосса.
        """
        optimizer.zero_grad()
        loss.backward(retain_graph=True)
        MAG = opt_img.grad.detach().abs().mean().item()
        # opt_img.grad.zero_()
        return MAG

    # def recalc_MAGs_for_style_only(MAGs):
    #     MAGs = MAGs[:-1]
    #     return MAGs / MAGs.sum() * 100

    def set_style_weights_to_wanted() -> None:
        """
        Меняет веса стилевых функций потерь так, чтобы вклады стилевых функций
        потерь были равны заданным в wanted_style_losses_contrib.

        Returns
        -------
        None
            Функция только меняет веса и ничего не возвращает.
        """
        style_losses, content_loss, tv_loss = calc_losses()

        style_MAGs = torch.tensor([calc_MAG(loss) for loss in style_losses], device=core.device)
        cur_losses_contrib = style_MAGs / style_MAGs.sum()

        cur_wanted_style_losses_contrib = []
        # if len(style_params.loss_layers) < 5:
        # Случай, когда стилевой лосс считается не на всех пяти слоях.
        for layer in style_params.loss_layers:
            layer_num = int(layer[1])
            cur_wanted_style_losses_contrib.append(wanted_style_losses_contrib[layer_num - 1])
        cur_wanted_style_losses_contrib = torch.tensor(cur_wanted_style_losses_contrib, device=core.device)
        # cur_wanted_style_losses_contrib /= cur_wanted_style_losses_contrib.sum()
        # Не стоит перенормировать, так как иначе будем стилизовать в заданных слоях сильнее, чем предполагалось
        # else:
        #     cur_wanted_style_losses_contrib = wanted_style_losses_contrib

        # style.loss_weights = wanted_style_losses_contrib / cur_losses_contrib
        style_params.loss_weights = cur_wanted_style_losses_contrib / cur_losses_contrib
        if verbose >= 20 and print_iter is not False and cur_iter % print_iter == 0:
            print(
                f'Новые веса для стиля: {style_params.loss_weights.cpu().numpy()}'
                # f'доли весов: {100 * style.loss_weights / style.loss_weights.sum()}'
                # Это не вклады весов, это такие веса, чтобы вклады лоссов были такими, какие мы хотим
            )
        # TODO: FREE GRAPH? Вроде при выходе из скоупа сам должен очищаться.

    def content_style_equalization() -> None:
        """
        Меняет веса стилевых функций потерь так, чтобы уравнять силу наложения
        стиля и контента.

        Returns
        -------
        None
            Функция ничего не возвращает.
        """
        style_losses, content_loss, tv_loss = calc_losses()

        style_loss = torch.sum(style_params.loss_weights * style_losses)
        if content_params.loss_weight != 0:
            # Если не накладываем контент, то все равно нужно посчитать MAG для него,
            #  чтобы выровнить градиенты для стиля (чтобы они не были слишком
            #  маленькими или большими)
            content_loss *= content_params.loss_weight

        style_MAG = calc_MAG(style_loss)
        content_MAG = calc_MAG(content_loss)

        style_loss_weight_correction = stylization_strength * content_MAG / style_MAG
        style_params.loss_weights *= style_loss_weight_correction

        if verbose >= 20 and print_iter is not False and cur_iter % print_iter == 0:
            print(
                f'Оцененный коэффициент для стиля: {content_MAG / style_MAG:0.9f}\n'
                f'Итоговый коэффициент для стиля (с учетом силы стилизации): {style_loss_weight_correction:0.9f}\n'
                f'Скорректированные веса для стиля: {style_params.loss_weights.cpu().numpy()}'
            )

    def losses_contribution_measurement() -> None:
        """
        Считает вклады слоев в итоговую функцию потерь и сохраняет результаты в all_MAGs.

        Returns
        -------
        None
            Функция ничего не возвращает.
        """
        style_losses, content_loss, tv_loss = calc_losses()
        style_losses *= style_params.loss_weights
        content_loss *= content_params.loss_weight

        style_MAGs = torch.tensor([calc_MAG(loss) for loss in style_losses])
        content_MAG = torch.tensor([calc_MAG(content_loss)])

        cur_MAGs = torch.cat([style_MAGs, content_MAG])
        sum_MAG = cur_MAGs.sum()
        cur_MAGs /= sum_MAG
        all_MAGs.append(cur_MAGs)

        if verbose >= 100:
            to_print = 'Style: '
            to_print += ', '.join([f'{f"{MAG.item():0.3f}":>7}' for MAG in 100 * style_MAGs / sum_MAG])
            to_print += ', content: '
            to_print += f'{f"{(100 * content_MAG / sum_MAG).item():0.3f}":>7}'
            print(to_print)

            to_print = 'Style: '
            to_print += ', '.join([
                f'{f"{MAG.item():0.3f}":>7}'
                for MAG in 100 * style_MAGs / style_MAGs.sum()
            ])
            # to_print += ', content: '
            # to_print += f'{f"{(100 * content_MAG / sum_MAG).item():0.3f}":>7}'
            print(to_print)
        if verbose >= 150:
            print(f'MAGs | style: {style_MAGs.sum().item()}, content: {content_MAG.item()}')

    def print_and_update_history(loss: torch.Tensor) -> None:
        """
        Обновляет информацию в history, выводит информацию и изображения
        на экран, сохраняет стилизацию в images (с проверкой необходимых
        разрешений типа частоты обновления информации и т.п.).

        Parameters
        ----------
        loss : torch.Tensor
            Значения функции потерь для логирования.

        Returns
        -------
        None
            Функция ничего не возвращает.
        """
        nonlocal start_time_for_print, start_time_for_history

        if print_iter is not False and cur_iter % print_iter == 0:
            end_time = time.time()
            print(
                f'Iteration: {cur_iter}, '
                f'loss: {loss.item():0.3f}, '
                f'last {print_iter} iters time: {end_time - start_time_for_print}, '
                f'avg iter time: {(end_time - start_time_for_print) / print_iter}'
            )
            start_time_for_print = end_time

        if show_iter is not False and cur_iter % show_iter == 0:
            IU.show_pic_7x7(opt_img)

        if history_update_freq is not False and cur_iter % history_update_freq == 0:
            history['n_iter'].append(cur_iter)
            history['loss'].append(loss.item())
            end_time = time.time()
            history['time'].append(end_time - start_time_for_history)
            start_time_for_history = end_time

        if return_gif:
            images.append(IU.postprocessing(opt_img))

    def closure() -> torch.Tensor:
        """
        Один цикл оптимизации стилизуемого изображения.

        Returns
        -------
        loss : torch.Tensor
            Значение функции потерь.
        """
        nonlocal cur_iter, cur_losses
        cur_iter += 1

        # Новая итерация, поэтому обнуляем кэш с функциями потерь.
        cur_losses = None

        if wanted_style_losses_contrib is not None:
            set_style_weights_to_wanted()

        if equalize_content_and_style:
            content_style_equalization()

        if measure_losses_contribution:
            losses_contribution_measurement()

        loss = calc_loss()

        optimizer.zero_grad()
        loss.backward()

        print_and_update_history(loss)

        return loss


    # Начинаем обучение
    cur_iter = 0
    start_time_for_history = start_time_for_print = time.time()
    try:
        optimizer = optim.LBFGS([opt_img])
        # optimizer = optim.Adam([opt_img], lr=1)
        # lr_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=80, gamma=0.9)

        while cur_iter < max_iter:
            optimizer.step(closure)
            # lr_scheduler.step()
    except KeyboardInterrupt:
        print(f'Процесс переноса стиля был прерван пользователем на {cur_iter} итерации')
    # except MemoryError:
    #     warnings.warn(f'Процесс переноса стиля был прерван из-за ошибки памяти на {cur_iter} итерации')

    return Namespace(
        opt_img=IU.postprocessing(opt_img) if postprocess_opt_image else opt_img,
        history=history,
        images=images,
        all_MAGs=all_MAGs
    )


def full_style_transfer(load_images_args, load_images_kwargs, LWT_kwargs, style_transfer_kwargs) -> Namespace:
    """
    Процесс переноса стиля с нуля и до результата. Принимает все нужные
    аргументы и на выходе получается стилизация.

    Parameters
    ----------
    load_images_args
        Аргументы для функции загрузки изображений
        image_utils.load_and_prepare_images.
    load_images_kwargs
        Именованные аргументы для функции загрузки изображений
        image_utils.load_and_prepare_images.
    LWT_kwargs
        Именованные аргументы для функции make_losses_weigths_targets.
    style_transfer_kwargs
        Именованные аргументы для функции переноса стиля style_transfer.

    Returns
    -------
    Namespace
        Результаты процесса переноса стиля.
        Namespace с полями style, content и всеми полями, которые возвращает
        функция style_transfer.
        1. style : torch.Tensor
            Стилевое изображение.
        2. content : torch.Tensor
            Контентное изображение.
    """
    style, content, opt_img = IU.load_and_prepare_images(*load_images_args, **load_images_kwargs)
    if style_transfer_kwargs.get('verbose', 100) >= 10:
        IU.show(style, content, opt_img)

    vgg = VGG.get_vgg_instance()
    style_loss_params, content_loss_params = make_losses_weigths_targets(style, content, vgg=vgg, **LWT_kwargs)

    results = style_transfer(opt_img, style_loss_params, content_loss_params, vgg=vgg, **style_transfer_kwargs)

    return Namespace(
        style=style,
        content=content,
        **vars(results)
        # opt_img=opt_img,
        # history=results.history,
        # images=results.images,
        # all_MAGs=results.all_MAGs,
    )
