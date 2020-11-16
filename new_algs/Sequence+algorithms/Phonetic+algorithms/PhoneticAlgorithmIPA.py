import json
import re
import copy
import os
import csv
from collections import defaultdict
import itertools
import pkg_resources


def __open_json__(file):
    """
    Открывает json файлы
    """
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


class Node(object):
    """
    Класс для автоматического анализа звуков
    """
    def __init__(self, value=''):
        self.previous = None
        self.vector = value
        self.value = value
        self.affr = False
        self.next = None
        self.dift = False
        self.dia = {}


def clean(text):
    """
    Функция удаляет все знаки препинания
    """

    global dia

    text = text.lower()
    text = text.translate(str.maketrans('', '', dia))
    return text


def truncate(n, decimals=0):
    """
    Функция для сокращения символов после запятой
    """
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def type_letter(item, vows, cons):

    """
    Функция, которая определяет тип звука: гласный / согласный
    """

    if isinstance(item, list):
        if isinstance(item[0], str): return type_letter(item[0], vows, cons)
        elif isinstance(item[0], tuple):
            if item[0][4] == '+': return 'vow'
            elif item[0][4] == '-': return 'cons'

    elif item in vows: return 'vow'
    elif item in cons: return 'cons'

    return 'None'


def mean(a, b):
    """
    Функция для расчета среднего значения
    """
    return (a + b) / 2


def no(a, b):
    """
    Функция для отсутсвия нормализации
    """
    return 1


def default_default():

    """
    Открытие всех нужных файлов
    """

    global filenames

    with open(filenames[0], 'r', encoding='utf-8') as f:
        reg_all_sounds, reg_comb, dia = f.readlines()
        reg_all_sounds, reg_comb, dia = reg_all_sounds[:-1], reg_comb[:-1], dia[:-1]

    diacrit, cons, vows = [__open_json__(i) for i in filenames[1:4]]
    pattern1 = re.compile(reg_comb)
    pattern2 = re.compile(reg_all_sounds)

    return reg_all_sounds, reg_comb, dia, diacrit, cons, vows, pattern1, pattern2


resource = 'phonetic_algorithmIPA'
res = ['regs.txt', 'diacrit.json', 'cons.json', 'vows.json', 'ftable.json', 'index_column.json', 'rows.json']
paths = ['/'.join(('data', i)) for i in res]
filenames = [pkg_resources.resource_filename(resource, path) for path in paths]

normal_func = {'mean': mean, 'max': max, 'min': min, False: no}
reg_all_sounds, reg_comb, dia, diacrit, cons, vows, pattern1, pattern2 = default_default()


class PhoneticAlgorithmIPA:

    def __init__(self):

        self.default_settings(user=False)

    def default_settings(self, user=True):
        """
        Восстанавливаем дефолтные настройки
        """

        if user:
            global reg_all_sounds, reg_comb, dia, diacrit, cons, vows, pattern1, pattern2
            reg_all_sounds, reg_comb, dia, diacrit, cons, vows, pattern1, pattern2 = default_default()

        self.feature_table = __open_json__(filenames[4])
        self.column_index = __open_json__(filenames[5])
        self.row = __open_json__(filenames[6])

        self.feature = {}

    def __combination_splitter__(self, word):
        '''
        Готовит строку к анализу, заменяет комбинации символов
        '''
        word = clean(word)
        length = len(word)
        res = re.findall(pattern1, word)

        if res != []:
            word = re.sub(pattern1, '@', word)
        word = word[::-1] + '#'

        return word, res, length

    def __dia_cond1__(self, current, vows, cons, step, value):

        """
        Проверка на дифтонг раз
        """
        a = type_letter(current.value, vows, cons) == 'vow'
        b = current.previous is not None

        if a and b:
            c = type_letter(current.previous.value, vows, cons) == 'vow'
            d = not current.previous.dia.get('stress')
            e = not current.previous.dia.get('secondaty stress')
            f = isinstance(current.previous.value, list) and len(current.previous.value) < 3
            j = not isinstance(current.previous.value, list)

            if c and d and e:
                if f or j:
                    current.affr = True

        return current

    def __dia_applier__(self, current, step, vows, cons):
        """
        Меняет вектор значений
        """
        if isinstance(current.value, list): return current.vector

        if current.dia != {}:

            for value in current.dia:

                current.vector[self.column_index[value]] = current.dia[value]

                if step == 0 and value == 'syllabic' and current.dia[value] == '-':
                    current = self.__dia_cond1__(current, vows, cons, step, value)

        current.vector = tuple(current.vector)

        return current.vector

    def __add_value__(self, current, answer, letter, step, vows, cons):
        """
        Добавляет в ответ вектор значений звука
        """

        answer.append(current.vector)
        cur = current

        if current.next is None:
            current.next = Node()

        current = current.next
        current.previous = cur

        return current

    def __post_diacrit__(self, index, length, current, value, letter):
        """
        Проверка на дикритики, которые идут после звука
        """

        if index == length - 1: raise ValueError('Wrong location of {}'.format(letter))

        if current.value == '':
            if letter == '̯': current.dift = True
            current.dia = {**current.dia, **value[1]}

        else:
            if current.next is None: current.next = Node()
            if letter == '̯': current.next.dift = True
            current.next.dia = {**current.next.dia, **value[1]}

        return current

    def __between_diacrit__(self, index, length, current, step):

        """
        Проверка на дикритики, которые идут между звуками
        """

        if 0 < index != length - 1:

            if current.next is None: current.next = Node()

            current.next.affr = True

            if isinstance(current.value, str):
                current.vector = self.__dia_applier__(current, step, vows, cons)
                current.vector = [current.vector]
                current.value = [current.value]
                current.dift = [current.dift]

        else: raise ValueError

        return current

    def __diacritics__(self, letter, index, length, current, step, diacrit):

        """
        Обрабатывает диакритики
        """

        value = diacrit[letter]  # 'ⁿ': ['post', {'nasal': '+'}]

        if value[0] == 'post':
            current = self.__post_diacrit__(index, length, current, value, letter)

        elif value[0] == 'pre':
            if current.value == '': raise ValueError('Wrong position for {}'.format(letter))
            current.dia = {**current.dia, **value[1]}

        elif value[0] == 'between':
            current = self.__between_diacrit__(index, length, current, step)
        return current

    def __stress_number__(self, length, word, index, number, current):

        """
        Определяет кол-во ударных элементов
        """

        v = 'The stress is presented incorrectly'

        if number == 0: raise ValueError(v)

        if length-1-index < number+1 or word[index+1] not in ('_', '='):
            raise ValueError(v)

        if word[index+1] == '_': typ = 'main'
        elif word[index+1] == '=': typ = 'side'

        return [number, number, typ]

    def __stress_app__(self, letter, step, current, answer, vows, cons):

        """
        Работает с ударными звуками
        """

        if type_letter(current.value, vows, cons) != 'vow':
            raise ValueError('A non vowel element is under stress')

        if step[0] == step[1] and step[0] != 1:
            current.value = [current.value]
            current.vector = [current.vector]
            current.dift = [current.dift]

        elif step[0] != step[1]:
            current.value = current.previous.value + [current.value]
            current.vector = current.previous.vector + [current.vector]
            current.dift = current.previous.dift + [current.dift]
            current.previous = current.previous.previous
            answer.pop()

        if step[0] == 1: step = 0
        else: step[0] -= 1

        return step

    def __affricate__(self, current, answer, vows, cons):

        """
        Работает с аффрикатами
        """

        current.vector = [current.vector]
        current.value = [current.value]
        current.dift = [current.dift]

        if not isinstance(current.previous.value, list):
            current.previous.value = [current.previous.value]
            current.previous.vector = [current.previous.vector]
            current.previous.dift = [current.previous.dift]

        current.vector += current.previous.vector
        current.value += current.previous.value
        current.dift += current.previous.dift

        if len({type_letter(i, vows, cons) for i in current.value}) != 1:
            raise ValueError('All values should be have the same type')

        current.previous = current.previous.previous
        answer.pop()
        return current

    def __digit_rule__(self, letter, step, current, answer, vows, cons):

        """
        Добавляет предыдущий элемент в ответ, если дальше идет ударный звук
        """

        if step != 0 and step[0] != 1: raise ValueError('The stress is presented incorrectly')

        current, step = self.__letter_parser__(step, current, '', answer, vows, cons)

        return current, step

    def __dia_cond2__(self, current, vows, cons):

        """
        Проверка на дифтонг 2
        """

        if not current.dia.get('syllabic') and current.previous is not None:

            a = type_letter(current.previous.value, vows, cons) == 'vow'
            a0 = current.previous.dia.get('syllabic') == '-'
            b = not current.previous.dia.get('stress')
            b1 = not current.previous.dia.get('secondaty stress')
            c = isinstance(current.previous.value, list) and False not in current.previous.dift
            d = not isinstance(current.previous.value, list)

            if a and a0 and b and b1:
                if c or d:
                    current.affr = True
        return current

    def __letter_parser__(self, step, current, letter, answer, vows, cons, dig=False):

        """
        Обрабатывает МФА
        """

        if step != 0:
            if step[-1] == 'main': current.dia['stress'] = '+'
            else: current.dia['second stress'] = '+'

        if current.value != '':
            current.vector = self.__dia_applier__(current, step, vows, cons)

            if step == 0 and type_letter(current.value, vows, cons) == 'vow':
                current = self.__dia_cond2__(current, vows, cons)

            if step != 0:
                step = self.__stress_app__(letter, step, current, answer, vows, cons)

            if current.affr:
                current = self.__affricate__(current, answer, vows, cons)

            current = self.__add_value__(current, answer, letter, step, vows, cons)

        if letter not in ('#', ''):
            current.value = letter
            current.vector = copy.copy(self.feature_table[letter])

        return current, step

    def __conditions__(self, word, diac, vow, con):

        '''
        Проверяет корректность входных данных, если пользователь сам решил
        разделить транскрипции на звуки
        '''

        global diacrit

        typs = [type(i) for i in [word, diac, vow, con]]
        if typs != [str, dict, list, list]:
            raise ValueError('Wrong input data')

        typs = {isinstance(i, str) for i in vow}
        if typs != {True}:
            raise ValueError('Wrong vowel representaion')

        typs = {isinstance(i, str) for i in con}
        if typs != {True}:
            raise ValueError('Wrong consonant representaion')

        if diac != {} and diac != diacrit:
            for name in diac:
                self.__check_diacrit__(name, diac[name])

    def transcription_splitter(self, word, diacrit, vows, cons, user=True):

        if user:
            self.__conditions__(word, diacrit, vows, cons)

        """
        Делит транскрипцию на МФА элементы
        """

        if word == '': return ''

        word, replacements, length = self.__combination_splitter__(word)

        answer = []
        current = Node()
        step, index_replace = 0, 0

        for index, letter in enumerate(word):

            if letter == '@':
                letter = replacements
                [index_replace]
                index_replace += 1

            if letter in ('_', '='): continue

            if letter.isdigit():
                if current.value != '':
                    current, step = self.__digit_rule__(letter, step, current, answer, vows, cons)
                step = self.__stress_number__(length, word, index, int(letter), current)

            elif letter in diacrit:
                current = self.__diacritics__(letter, index, length, current, step, diacrit)

            elif letter in self.row or letter == '#':
                current, step = self.__letter_parser__(step, current, letter, answer, vows, cons)

            else: return False

        return answer[::-1]

## --------------------------------------------------------

    def __check_vector__(self, vector):

        '''
        Проверяет корректность входных данных, если пользователь сам решил
        посчитать расстояние между векторами
        '''

        if not isinstance(vector, tuple):
            raise ValueError('Wrong vector type')

        wrng = [value for value in vector if value not in ('+', '-', '0')]
        if wrng != []:
            raise ValueError("Vectors should contain only +, -, 0")

    def sound_dist(self, a, b, user=True):

        """
        Рассчитывет расстояния между двумя векторами
        """

        if user:
            self.__check_vector__(a)
            self.__check_vector__(b)
            if len(a) != len(b):
                raise ValueError('Vectors should have equal length')

        similar, common, uncommon = 0, 0, 0

        for index, item in enumerate(a):

            if item == b[index] and item != '0':
                common += 1
                similar += 1

            elif item != b[index]:
                if item == '0' or b[index] == '0': uncommon += 1
                else: common += 1

        dist = 1 - (similar / (common + (uncommon * 2)))
        return dist

    def __different_length__(self, a, len_a, b, len_b):

        """
        Рабоатет с комплексами разной длины
        """

        res = []

        if len_a < len_b:
            a, b = b, a
            len_a, len_b = len_b, len_a

        for i in a:
            r = [self.sound_dist(i, l, user=False) for l in b]
            res.append(min(r))

        ans = sum(sorted(res)[:min(len_a, len_b)])

        return ans + len_a - len_b

    def __equal_length__(self, a, b):

        """
        Работает с комплексами одной длины
        """

        res = [self.sound_dist(it, b[ind], user=False) for ind, it in enumerate(a)]

        return sum(res)

    def __dist_affr__(self, a, b):
        """
        Рассчитывает расстояние между комплексами звуков
        """

        len_a, len_b = len(a), len(b)

        if len_a != len_b:
            return self.__different_length__(a, len_a, b, len_b)

        return self.__equal_length__(a, b)

    def __phone_dist__(self, a, b):
        """
        Определяет с какими данными мы рабоаем
        """

        if isinstance(a, list) and isinstance(b, list):
            return self.__dist_affr__(a, b)

        if isinstance(a, list) and not isinstance(b, list):
            return self.__dist_affr__(a, [b])

        if isinstance(b, list):
            return self.__dist_affr__([a], b)

        return self.sound_dist(a, b, user=False)

    def __check_lev_lists__(self, a, b):

        '''
        Проверяет корректность входных данных, если пользователь сам решил
        посчитать расстояния по Левенштейну
        '''

        lengths = set()

        for value in [a, b]:

            if not isinstance(value, list):
                raise ValueError('Wrong data type')

            if value == []:
                raise ValueError('Wrong data entry')

            for item in value:
                self.__check_vector__(item)
                lengths.add(len(item))

        if len(lengths) != 1:
            raise ValueError('All vectors should be the same length')

    def lev_distance(self, a, b, user=True):

        """
        Модифицированное расстояние Дамерау-Левенштейна
        """

        # Первыми - строчки
        # столбики - слово b

        if user:
            self.__check_lev_lists__(a, b)

        dis = [[0] * (len(b)+1) for _ in range(len(a)+1)]
        size = (len(b)+1) * (len(a)+1)
        i, row, col = 0, 0, 0

        while i < size:

            if row == 0:
                if col != 0:
                    dis[row][col] = dis[row][col-1] + 1

            elif col == 0:
                if row != 0:
                    dis[row][col] = dis[row - 1][col] + 1

            elif row > 2 and col > 2 and a[row-1] == b[col-2] and a[row-2] == b[col-1]:
                dis[row][col] = dis[row - 3][col - 3] + 1

            else:
                dis[row][col] = min([dis[row][col - 1] + 1,  # левый
                                dis[row - 1][col - 1] + self.__phone_dist__(a[row-1], b[col-1]),  # диаг
                                dis[row - 1][col] + 1])  # верхний

            col += 1
            i += 1

            if col == len(b) + 1:
                col = 0
                row += 1

        return dis[len(a)][len(b)]

## --------------------------------------------------------

    def __check_data__(self, data, normalize):
        """
        Проверяет данные на коректрность, делит на элементы, выдает расстояния
        """

        global diacrit, vows, cons

        dists = []

        for line in data:
            
            if len(line) != 2:
                raise ValueError('Wrong row number. Check your delimiter')

            if line[0] == line[1]: dist = 0
            else:
                a = self.transcription_splitter(line[0], diacrit, vows, cons, user=False)
                b = self.transcription_splitter(line[1], diacrit, vows, cons, user=False)
                
                if a is False or b is False:
                    print('Wring values in line: {}'.format(str(line)))
                    dist = None
                else:
                    if a == '': dist = len(b)
                    elif b == '': dist = len(a)
                    else: dist = self.lev_distance(a, b, user=False)

                    dist /= normal_func.get(normalize)(len(a), len(b))

            if dist is not None:
                dists.append(dist)

        return dists

    def phonetic_distance(self, path, delimiter=';', typ='Non LS', total_dist=False,
                          irrelevant_features=[], normalize=False):

        """
        Открывает файл с транскрипциями, возвращает расстояния
        """

        if not path.endswith('.csv'):
            raise ValueError('Incorrect file type. It should be csv')

        if not os.path.isfile(path):
            raise ValueError('Incorrect file path')

        if typ not in ('LS', 'Non LS'):
            raise ValueError('Incorrect type argument')

        if not normal_func.get(normalize):
            raise ValueError('Incorrect normalization argument')

        if not isinstance(irrelevant_features, list):
            raise ValueError('Wrong irrelevant_features data type')

        if not isinstance(total_dist, bool):
            raise ValueError('total_dist can only be True or False')

        if delimiter == '':
            raise ValueError('Delimiter should be filled')

        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            data = list(reader)

        if typ == 'LS': self.__ls_dist_matrix__(data, irrelevant_features)

        elif irrelevant_features != []:
            raise ValueError('If you want to delete irrelevant features, use "LS" type!')

        dist = self.__check_data__(data, normalize)

        return dist

## --------------------------------------------------------

    def __stressed__(self, line):

        """
        Заменяет все ударные элементы на *
        """

        reg2 = '.{%s}(?:_|=)%s'

        n = re.findall('(?:_|=)[1-9]', line)

        for i in n:
            le = i[-1]
            line = re.sub(reg2 % (le, le), '*' * (int(le) + 2), line)

        return line

    def __right_part__(self, index, len_right, line, right_rule, word, cons_u, vows_u):
        """
        Обрабатывает правый контекст правила
        """

        global cons, vows

        if right_rule == '': return True

        idx = index + 1
        length = len(line) - 1

        while len_right > 0:

            if idx > length: break

            if line[idx] in ('_', '=') or line[idx].isdigit(): idx += 1

            else:

                if right_rule[-len_right] in self.feature_table:
                    if right_rule[-len_right] in vows_u or right_rule[-len_right] in cons_u:
                        l = line
                    else: l = word
                else: l = line

                if right_rule[-len_right] == '@':
                    if vows_u == []: raise ValueError('Enter vowels')
                    if l[idx] not in vows_u and word[idx] not in vows:
                        return False

                elif right_rule[-len_right] == '&':
                    if cons_u == []: raise ValueError('Enter consonants')
                    if l[idx] not in cons_u and word[idx] not in cons:
                        return False

                elif right_rule[-len_right] != l[idx]:
                    return False

                idx += 1
                len_right -= 1

        if len_right != 0:
            return False
        return True

    def __left_part__(self, index, len_left, line, left_rule, word, cons_u, vows_u):

        """
        Обрабатывает левый контекст правила
        """

        global cons, vows

        if left_rule == '': return True

        idx = index - 1

        while len_left > 0:

            if idx < 0: break

            if line[idx] in ('_', '=') or line[idx].isdigit(): idx -= 1

            else:

                if left_rule[len_left-1] in self.feature_table:
                    if left_rule[len_left-1] in vows_u or left_rule[len_left-1] in cons_u:
                        l = line
                    else: l = word
                else: l = line

                if left_rule[len_left-1] == '@':
                    if vows_u == []: raise ValueError('Enter vowels')
                    if l[idx] not in vows_u and word[idx] not in vows:
                        return False

                elif left_rule[len_left-1] == '$':
                    if cons_u == []: raise ValueError('Enter consonants')
                    if l[idx] not in cons_u and word[idx] not in cons:
                        return False

                elif left_rule[len_left-1] != l[idx]:
                    return False

                idx -= 1
                len_left -= 1

        if len_left != 0:
            return False
        return True


    def __rule_applier__(self, rules_dict, word, cons_u=[], vows_u=[]):
        """
        Применяет правила трансформаций
        """

        res = [''] * len(word)
        count = 0

        while True:

            for index, letter in enumerate(word):

                ans = letter
                line = word
                
                if letter not in ('_', '=') or not letter.isdigit():

                    rules = rules_dict.get(letter)

                    if rules:

                        for value, rule in rules:

                            if rule == '': ans = value

                            elif '_' in rule:

                                if '*' in rule: line = self.__stressed__(word)

                                left, right = rule.split('_')

                                left = self.__left_part__(index, len(left), line, left, res, cons_u, vows_u)
                                right = self.__right_part__(index, len(right), line, right, res, cons_u, vows_u)

                                if left and right:
                                    count += 1
                                    ans = value
                            else:
                                raise ValueError('Wrong rule: {}'.format(rule))

                res[index] = ans

            if count == 0: break
            else:
                count = 0
                word = res

        return ''.join(res[1:-1])

    def __rule_collector__(self, rules_dict):
        """
        Группирует правила по буквам
        """

        d = defaultdict(list)

        for line in rules_dict:

            if len(line) != 3:
                raise ValueError('There have to be 3 columns')

            if len(line[0]) != 1:
                raise ValueError('Grapheme should be 1 symbol long')

            res = re.findall('\{(.*?)\}', line[2])
            
            if res != []:
                a = re.sub('\{(.*?)\}', '{}', line[2])
                res = [i.split(',') for i in res]
                for i in itertools.product(*res, repeat=1):
                    d[line[0]].append([line[1], a.format(*i)])
            else:
                d[line[0]].append([line[1], line[2]])

        return d

    def phonetic_transformer(self, data_path, rules_path, delimiter=';', typ='Non LS', irrelevant_features=[],
                             normalize=False, total_dist=False, cons_u=[], vows_u=[]):

        """
        Трансформирует строки в их фонетические представления

        Чувствителен к регистру
        """

        if not data_path.endswith('.csv') or not rules_path.endswith('.csv'):
            raise ValueError('Incorrect data type. It should be csv')

        if not os.path.isfile(data_path) or not os.path.isfile(rules_path):
            raise ValueError('Incorrect file path')

        if not normal_func.get(normalize):
            raise ValueError('Incorrect normalization argument')

        if typ not in ('LS', 'Non LS'):
            raise ValueError('Incorrect type argument')

        if not isinstance(irrelevant_features, list):
            raise ValueError('Wrong irrelevant_features data type')

        if not isinstance(total_dist, bool):
            raise ValueError('total_dist can only be True or False')

        if delimiter == '':
            raise ValueError('Delimiter should be filled')

        if not isinstance(vows_u, list):
            raise ValueError('Vows should be list')

        if not isinstance(cons_u, list):
            raise ValueError('Cons should be list')

        if vows_u != [] and {isinstance(i, str) for i in vows_u} != {True}:
            raise ValueError('Incrorrect vows_u type')

        if cons_u != [] and {isinstance(i, str) for i in cons_u} != {True}:
            raise ValueError('Incrorrect vows_u type')

        with open(rules_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            rules = list(reader)

        with open(data_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            data = list(reader)

        rules_dict = self.__rule_collector__(rules)

        res = []

        for line in data:

            l = self.__rule_applier__(rules_dict, '#' + clean(line[0]) + '#', cons_u, vows_u)
            r = self.__rule_applier__(rules_dict, '#' + clean(line[1]) + '#', cons_u, vows_u)
            res.append((l, r))

        if typ == 'LS': self.__ls_dist_matrix__(res, irrelevant_features)

        elif typ == 'Non_LS' and irrelevant_features != []:
            raise ValueError('If you want to delete irrelevant features, use "LS" type!')

        dist = self.__check_data__(res, normalize)

        if total_dist is True:
            return dist, mean(total_dist)
        return dist

## --------------------------------------------------------

    def __users_irr_features__(self, irrelevant_features):

        """
        Обрабатывает нерелевантные признаки пользователя
        """

        for i in irrelevant_features:
            if i not in self.column_index:
                raise ValueError('Incorrect irrelevant features')
        self.features = irrelevant_features

    def __detect_irr_features__(self, data):

        """
        Находит нерелевантные признаки
        """

        index = 0

        for line in data:
            for word in line:
                for ph in pattern2.findall(word):
                    res = {ind for ind, item in enumerate(self.feature_table[ph]) if item == '0'}
                    if index == 0: self.features = res
                    else: self.features &= res
                index += 1

    def __ls_dist_matrix__(self, data, irrelevant_features):

        """
        Меняет таблицу соответсвий звуков и признаков с учетом нерелевантных значений
        """

        if irrelevant_features != []:
            self.__users_irr_features__(irrelevant_features)

        else: self.__detect_irr_features__(data)

        if self.features != {}:
            for i in self.feature_table:
                x = self.feature_table[i]
                for l in self.features: x.pop(self.column_index[l])
                self.feature_table[i] = x

            index = 0
            d = {}
            for i in self.column_index:
                if i not in self.features:
                    d[i] = index
                    index += 1
            self.column_index = d
            self.features = {}

    def add_columns(self, d):
        '''
        Добавляет колонку (признак)
        sonorant: [+ - 0]
        '''

        if not isinstance(d, dict):
            raise ValueError('Incorrect data type')

        for name in d:

            values = d[name]

            if not isinstance(name, str):
                raise ValueError('Incorrect column name type')

            if not isinstance(values, list):
                raise ValueError('Incorrect column values type')

            if values == [] or name == '':
                raise ValueError('Wrong data type')

            if name in self.column_index:
                raise ValueError('Column already exists')

            if len(values) != len(self.feature_table):
                raise ValueError('All rows have to be filed')

            self.column_index[name] = len(self.column_index)

            for item in self.feature_table:
                value = values[self.row[item]]
                if value not in ('+', '-', '0'):
                    raise ValueError('Wrong data type')
                self.feature_table[item].append(value)

    def __finish_comp__(self, reg_comb, reg_all_sounds, pattern1, pattern2):

        """
        Меняет регулярые значения с учетом добавленных значений
        """

        pattern1 = re.compile(reg_comb)
        pattern2 = re.compile(reg_all_sounds)

    def add_rows(self, d):

        '''
        Добавляет звук

        a: [+ - 0]
        '''

        global reg_comb, pattern1, reg_all_sounds, cons, vows

        if not isinstance(d, dict):
            raise ValueError('Incorrect data type')

        for name in d:

            values = d[name]

            if not isinstance(name, str):
                self.__finish_comp__(reg_comb, reg_all_sounds, pattern1, pattern2)
                raise ValueError('Incorrect row value type')

            if not isinstance(values, list):
                self.__finish_comp__(reg_comb, reg_all_sounds, pattern1, pattern2)
                raise ValueError('Incorrect row values type')

            if values == [] or name == '':
                self.__finish_comp__(reg_comb, reg_all_sounds, pattern1, pattern2)
                raise ValueError('Wrong data type')

            if name in self.row:
                self.__finish_comp__(reg_comb, reg_all_sounds, pattern1, pattern2)
                raise ValueError('This sound already exists')

            if len(values) != len(self.column_index):
                self.__finish_comp__(reg_comb, reg_all_sounds, pattern1, pattern2)
                raise ValueError('All columns have to be filed')

            for val in values:
                if val not in ('+', '-', '0'):
                    self.__finish_comp__(reg_comb, reg_all_sounds, pattern1, pattern2)
                    raise ValueError('Wrong data type')

            self.row[name] = len(self.row)
            self.feature_table[name] = values

            if len(i) > 1: reg_comb += '|' + name
            reg_all_sounds += '|' + name

            if values[4] == '+': vows += name
            elif values[4] == '-': cons.add(name)

        self.__finish_comp__(reg_comb, reg_all_sounds, pattern1, pattern2)

    def __check_diacrit__(self, name, values):

        if not isinstance(name, str):
            raise ValueError('Incorrect row value type')

        if name in ('@', '_', '=', '#'):
            raise ValueError('{} can not be used'.format(name))

        if not isinstance(values, (list, tuple)):
            raise ValueError('Incorrect row values type')

        if len(values) != 2 or name == '':
            raise ValueError('Wrong data entry')

        if not isinstance(values[0], str) or not isinstance(values[1], dict):
            raise ValueError('Wrong data type')

        if values[0] not in ('pre', 'post', 'between'):
            raise ValueError('Wrong position type')

        if len(name) != 1:
            raise ValueError('Diacritic should be one item long')

        for feach in values[1]:
            if feach not in self.column_index:
                raise ValueError('Diacritic value should be in feature table')

            if values[1][feach] not in ('+', '-'):
                raise ValueError('Wrong diacritic value')

    def add_diacritics(self, d):
        '''
        Добавляет диакритику

        diacrit = {'ⁿ': ['post', {'nasal': '+'}]}
        '''

        global diacrit, dia

        if not isinstance(d, dict):
            raise ValueError('Incorrect data type')

        for name in d:
            values = d[name]

            if name in diacrit:
                raise ValueError('This diacritic already exists')

            self.__check_diacrit__(name, values)

            if name in dia: dia = dia.replace(name, '')

            diacrit[name] = values

    def __item_dict__(self, name, values):

        # d = {'a': [values]}

        if len(values) != len(self.column_index):
            raise ValueError('All columns have to be filed')
                    
        for value in values:
            if value not in ('+', '-', '0'):
                raise ValueError('Incorrect feature value')
                        
        self.feature_table[name] = values

    def __feature_dict__(self, name, values):

        ## d = {'feature': [values]}

        if len(values) != len(self.row):
            raise ValueError('All rows have to be filed')

        feature = self.column_index[name]

        for l in self.feature_table:
            value = values[self.row[l]]
            if value not in ('+', '-', '0'):
                raise ValueError('Incorrect feature value')
            self.feature_table[l][feature] = value

    def __partic_values__(self, name, values):

        for feature in values:
                    
            if feature not in self.column_index:
                raise ValueError('Incorrect feature name')

            if values[feature] not in ('+', '-', '0'):
                raise ValueError('Incorrect feature value')

            self.feature_table[name][self.column_index[feature]] = values[feature]

    def change_feature_table(self, d):
        
        '''
        d = {'a': {'feature': value}}
        d = {'a': [values]}
        d = {'feature': [values]}
        
        '''

        if not isinstance(d, dict):
            raise ValueError('Wrong data type')

        if d == {}:
            raise ValueError('Enter correct data')

        for i in d:
            
            if isinstance(d[i], list):  # d = {'feature': [values]}
                
                if i in self.column_index:
                    self.__feature_dict__(i, d[i])

                elif i in self.row:
                    self.__item_dict__(i, d[i])
                
                else: raise ValueError('Incorrect input data')
            
            elif isinstance(d[i], dict) and i in self.row:
                self.__partic_values__(i, d[i])
                    
            else: raise ValueError('Incorrect input data')

