import re
import numpy as np
import pandas as pd
import pkg_resources


resource_package = 'phonetic_algorithmRu'
res = ['distance_matrix.csv', 'data_all.csv', 'vows.csv', 'aff_.csv', 'cons_.csv', 'stress_data.csv']
paths = ['/'.join(('phon_data', i)) for i in res]
filenames = [pkg_resources.resource_filename(resource_package, path) for path in paths]

__dist_matrix__ = pd.read_csv(filenames[0], index_col='index')
__data__ = pd.read_csv(filenames[1], index_col='Unnamed: 0')
__vows__ = pd.read_csv(filenames[2], index_col='name')
__aff__ = pd.read_csv(filenames[3], index_col='name')
__cons__ = pd.read_csv(filenames[4], index_col='name')
__st_words__ = pd.read_csv(filenames[5], index_col='word')
__stop_words__ = ['а',  'без',  'близ',  'в',  'вне',  'во',  'вокруг',  'вслед',  'для',  'до',  'за',  'и',  'из',
              	  'изза',  'изо',  'изпод',  'к',  'ко',  'меж',  'между',  'мимо',  'на',  'над',  'о',  'об',  'обо',
              	  'около',  'от',  'ото',  'перед',  'передо',  'по', 'поверх',  'под',  'подо',  'понад',  'после',
             	  'пред',  'при',  'про',  'ради',  'с',  'сверх',  'сверху']
                                               

def __tokenize__(text):
    """
    Функция удаляет все знаки препинания.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text).replace('\n', '')
    text = re.sub(r'[\s]{2,}', ' ', text)
    return text.split(' ')


def __num_of_vowls__(word):
    """
    Функция считает кол-во гласных в слове
	
    >>> __num_of_vowls__('мама')
    2
    """
    num = len(re.findall('(а|е|ё|о|и|я|ю|у|ы|э)', word))
    if num:
        return num
    else:
        return 1


def __stressed__(word):
    """
    Функция определяет ударение в слове по словарю.
    Если слова в словаре нет, выдаются все возможные варианты.
	
    >>> [i for i in __stressed__('замок', __st_words__)]
    [2, 1]
    """

    try:
        a = __st_words__.loc[word]['stressed_s'].tolist()

        if isinstance(a, list):
            yield from a
        else:
            yield from [a]

    except KeyError:
        yield from ['None']
        

def __change__(word):
    """
    Замена сочетаний согласных
    """
    word = re.sub('(с|ст|сс|з|зд|ж|ш)ч', 'щ', word)
    word = re.sub('(с|зд|з)щ', 'щ', word)
    word = re.sub('(тч|тш|дш)', 'ч', word)
    word = re.sub('(с|з)ш', 'ш', word)
    word = re.sub('сж', 'ж', word)
    word = re.sub('(т|ть|д)с', 'ц', word)
    word = re.sub('(ст|сть)с', 'ц', word)
    return word
    

def __my_type__(letter):
    """
    Функция определяет тип входного символа: гласная, согласная, знак
    """
    if letter in __vows__.index:
        return 'v'
    
    if letter in __cons__.index:
        return 'c'
    
    if letter in ('ь', 'ъ'):
        return 'm'
    else:
        raise ValueError('Not Cyrillic')



def __due_to_vow_table__(ans, index, letter, stress, vow_n, length):
    """
    Функция преобразует гласные буквы в звуки в зависимости от позиции
    """

    if vow_n == stress:  # ударный

        if ans.value not in ('а', 'о', 'у', 'ы') and ans.next is not None and ans.next.type == 'c':

            if ans.value != 'э' and ans.next.value not in ('ш', 'ж', 'ц'):
                ans.next.soft = True
            elif ans.value in ('э', 'е') and ans.next.value in ('ш', 'ж', 'ц'):
                letter = 'э'
            elif ans.value == 'и':
                letter = 'ы'

        __j__(ans, letter, length, index, 'V')

    elif index == length - 1:  # начало
        __j__(ans, letter, length, index, '#')

    elif vow_n == stress + 1:  # первый предударный

        if ans.next is not None and ans.next.value in ('ц', 'ж', 'ш'):
            ans.value = __vows__.loc[letter]['v1_sh']

        elif letter in ('е', 'ё', 'и', 'ю', 'я'):
            ans.value = __vows__.loc[letter]['v1_soft']
            ans.next.soft = True
        elif ans.next is not None and ans.next.value in ('щ', 'ч', 'й'):
            ans.value = __vows__.loc[letter]['v1_soft']
        else:
            ans.value = __vows__.loc[letter]['v1_hard']

    elif vow_n >= stress + 2:  # второй предударный

        if ans.next is not None and ans.next.value in ('ц', 'ж', 'ш'):
            ans.value = __vows__.loc[letter]['v2_hard']

        elif ans.next is not None and ans.next.type == 'v':
            if letter in ('е', 'ё', 'и', 'ю', 'я'):
                ans.value = __vows__.loc[letter]['v1_soft']
            else:
                ans.value = __vows__.loc[letter]['v1_hard']

        elif letter in ('е', 'ё', 'и', 'ю', 'я'):
            ans.value = __vows__.loc[letter]['v2_soft']
            ans.next.soft = True

        elif ans.next is not None and ans.next.value in ('щ', 'ч', 'й'):
            ans.value = __vows__.loc[letter]['v2_soft']

        else:
            ans.value = __vows__.loc[letter]['v2_hard']

    elif vow_n < stress:  # заударные

        if ans.next is not None and ans.next.value in ('ц', 'ж', 'ш'):

            __j__(ans, letter, length, index, 'vn_hard')

        elif letter in ('е', 'ё', 'и', 'ю', 'я'):

            if vow_n == stress - 1 and ans.next is not None and ans.next.type == 'v':
                __j__(ans, letter, length, index, 'vn_soft')
            else:
                ans.value = __vows__.loc[letter]['vn_soft']
            ans.next.soft = True

        elif ans.next is not None and ans.next.value in ('щ', 'ч', 'й'):
            ans.value = __vows__.loc[letter]['vn_soft']

        else:
            if vow_n == stress - 1 and ans.next is not None and ans.next.type == 'v':
                __j__(ans, letter, length, index, 'vn_hard')
            else:
                ans.value = __vows__.loc[letter]['vn_hard']


def __j__(ans, letter, length, index, position):
    """
    Функция вставляет й в нужной позиции
    """

    ans.value = __vows__.loc[letter][position]

    if letter in ('ю', 'е', 'ё', 'я'):

        if index == length - 1:
            ans.j_ = True

        elif ans.next is not None and ans.next.type == 'v':
            ans.j_ = True

            if 'vn' in position:
                ans.value = __vows__.loc[letter]['vn_hard']

        elif ans.next is not None and ans.next.value in ('ь', 'ъ'):
            ans.j_ = True

            if 'vn' in position:
                ans.value = __vows__.loc[letter]['vn_hard']

    elif letter in ('и', 'о') and ans.next is not None and ans.next.value == 'ь':
        ans.j_ = True

        if 'vn' in position:
                ans.value = __vows__.loc[letter]['vn_hard']


def __cons_tranformer__(ans, letter, vcd=False):
    """
    Функция преобразует согласные буквы в звуки в зависимости от позиции
    """
	
    a = letter

    if letter in ('ч', 'ш', 'щ', 'ж'):
        ans.value = __cons__.loc[ans.value]['hard']
        if ans.__dict__.__contains__('soft'):
            del ans.soft
        if letter in ('ч', 'щ'):
            if ans.__dict__.__contains__('no_voice'):
                del ans.no_voice
            if ans.__dict__.__contains__('voice'):
                del ans.voice

    if ans.__dict__.__contains__('no_voice'):  # оглушение
        ans.value = __cons__.loc[ans.value]['no_voice']

    elif ans.__dict__.__contains__('voice'):  # озвончение
        ans.value = __cons__.loc[ans.value]['voiced']

    if vcd is True:
        if ans.previous is None:
            ans.value = __cons__.loc[ans.value]['voiced']

    if not vcd:
        if ans.previous is None:  # конец слова
            if ans.next is not None:
                ans.next.no_voice = True
            if __data__[ans.value]['vcd'] == '+':
                ans.value = __cons__.loc[ans.value]['no_voice']

    if ans.next is not None:
        if ans.value in __data__.columns and __data__[ans.value]['vcd'] == '-' and ans.next is not None:  # оглушение следующих

            if ans.next.value in __data__.columns and __data__[ans.next.value]['son'] == '-':
                ans.next.no_voice = True

        elif ans.value in __data__.columns and __data__[ans.value]['son'] == '-' and ans.value not in ('в', "в’") and __data__[ans.value]['vcd'] == '+':  # озвончение слудующих
            ans.next.voice = True

    if ans.previous is not None:

        if ans.previous.value == 'к' and letter == 'г':
            ans.value = 'х'

        elif ans.previous.value in (ans.value, ans.value + "’"):
            ans.value = ''

    if ans.__dict__.__contains__('soft'):  # смягчение
        ans.value = __cons__.loc[ans.value]['soft']


class Node(object):
    def __init__(self, value=''):
        self.value = value
        self.type = None
        self.previous = None
        self.next = None


def transcription(word, stress=False, separate=True, stop=False, vcd=False):

    """
    Фунция, которая определяет фонетическую транскриацию для
    слова с заданным ударением, расчитываемым с конца слова.

    Функция принимает 3 аргемента:
    i - type int, номер гласного, на который падает ударение
    (отсчет производится с конца слова).
    word - type str, слово, для которого должен произвожится разбор.

    >>> transcription(2, 'мама')
    ['м', 'а', 'м', 'ъ']

    >>> transcription(1, 'мама')
    ['м', 'а', 'м', 'а']
	
	>>> transcription('съехать', stress=2, separate=False)
	'сjехът’'

    Функция работает только с кириллическими символами. Если в слове содержатся не кириллические символы, вызывается ошибка.

    >>> transcription(2, 'papa')
    Traceback (most recent call last):
        ...
    ValueError: No vowles or not Cyrillic elements


    Если пользователь указывает номер гласной меньший кол-ва гласных,
    вызывается ошибка.

    >>> transcription(3, 'мама')
    Traceback (most recent call last):
        ...
    ValueError: There are only 2 vowel(s)
    """


    if not isinstance(word, str):
        raise ValueError('Wrong data type')

    if not isinstance(stress, int):
        raise ValueError('Wrong data type')

    if word == '':
        return ''

    word = word.lower()
    word = __tokenize__(word)

    if len(word) > 1:
        raise ValueError('Enter a word, not a phrase')

    word = word[0]
    nums = __num_of_vowls__(word)

    if stress:
        if nums < stress or stress < -1:
            raise ValueError('There are only {} vowel(s)'.format(str(__num_of_vowls__(word))))

    if not stress:
        stress = nums//2 + 1

    if stop is True:
        stress = -1

    letters = list(__change__(word))[::-1]

    ans = Node()
    head = ans
    prev = ans
    answer = []
    special = False
    length = len(letters)
    vow_n = 0

    for index, letter in enumerate(letters):

        if index == 0:
            ans.value = letter
            ans.type = __my_type__(letter)
            head = ans
        else:
            ans.previous = prev

        if index != length - 1:  # если не начало слова
            ans.next = Node(letters[index+1])
            ans.next.type = __my_type__(ans.next.value)

        if ans.type == 'v':  # гласные
            vow_n += 1
            __due_to_vow_table__(ans, index, letter, stress, vow_n, length)
            if ans.__dict__.__contains__('j_') and index == 0 and vow_n != stress:
                special = True

        elif ans.type == 'm':  # знаки

            if letter == 'ь':
                ans.next.soft = True
            ans.value = ''

        elif ans.type == 'c':  # согласные

            if letter == 'й':
                ans.value = 'ṷ'
            else:
                __cons_tranformer__(ans, letter, vcd=vcd)

        else:
            raise ValueError('Not Cyrillic')

        if ans.value == '' and index != 0:
            prev = ans.previous
        else:
            if ans.value != '':
                answer.append(ans.value)
            prev = ans

        if ans.__dict__.__contains__('j_'):
            if special:
                answer.append('ṷ')
                special = False
            else:
                answer.append('j')

        ans = ans.next

    if separate is False:
        return ''.join(answer[::-1])
    return answer[::-1]


def phrase_transformer(text, stresses=False, separate=True):
    """
    Функция трансформирует кириллическую строку в транскрипцию.
    Функция выдает массив всех возможных вариантов фонетического разбора.
    Если параметр separate == False, результатом будет массивы отдельных звуков. 
	
    >>> phrase_transformer('под')
    [[['п', 'о', 'т']]]
	
    >>> phrase_transformer('под сосной')
    [[['п', 'ъ', 'т'], ['с', 'а', 'с', 'н', 'о', 'ṷ']]]
	
    >>> phrase_transformer('под сосной', separate=False)
    [['път', 'сасноṷ']]
    """

    def combine(terms, accum):

        last = (len(terms) == 1)
        n = len(terms[0])

        for i in range(n):
            item = accum + [terms[0][i]]

            if last:
                combinations.append(item)
            else:
                combine(terms[1:], item)

    if not isinstance(text, str):
        raise ValueError('Wrong data type')
    
    if text == '':
        return ''

    words = __tokenize__(text)

    if stresses:
        if not isinstance(stresses, list):
            raise ValueError('Wrong data type')

        if len(words) != len(stresses):
            raise ValueError('The number of stresses must be the same as the number of words')

        if not all(isinstance(x, int) for x in stresses):
            raise ValaueError('The stress values type must be int')

    answer = []
    combinations = []
    length = len(words)

    for index, word in enumerate(words):

        stop = False
        vcd = False  # озвончение, если это фраза

        if word in __stop_words__ and length > 1:

            stop = True
            if index+1 <= len(words)-1 and words[index+1][0] in __data__.columns and __data__[words[index+1][0]]['vcd'] == '+':
                vcd = True

        answer.append([])

        if stresses:

            if separate is False:
                answer[-1].append(''.join(transcription(word, stop=stop, vcd=vcd, stress=stresses[index])))
            else:
                answer[-1].append(transcription(word, stop=stop, vcd=vcd, stress=stresses[index]))

        else:
            for stress in __stressed__(word):

                if stress == 'None':
                    if separate is False:
                        answer[-1].append(''.join(transcription(word, stop=stop, vcd=vcd)))
                    else:
                        answer[-1].append(transcription(word, stop=stop, vcd=vcd))

                elif separate is False:
                    answer[-1].append(''.join(transcription(word, stop=stop, vcd=vcd, stress=stress)))
                else:
                    answer[-1].append(transcription(word, stop=stop, vcd=vcd, stress=stress))

    combine(answer, [])
    return combinations

def __lev_distance__(a, b):

    """
	Расстояние Левенштейна для двух транскрипций. 
	Штраф за перестановки, удаление, вставку символа - 1. 
	Штраф за замену - расстояние между двумя звуками, вычисляемом по формуле: 
			1 - S_rows/ C_rows + Unc_rows*2
    """

    dis = np.zeros((len(a) + 1, len(b) + 1))
    i = 0
    row = 0
    col = 0

    while i < dis.size:

        if row == 0:
            if col != 0:
                dis[row, col] = dis[row, col-1] + 1

        elif col == 0:
            if row != 0:
                dis[row, col] = dis[row - 1, col] + 1

        elif row > 1 and col > 1 and a[row-1] == b[col-2] and a[row-2] == b[col-1]:
            dis[row, col] = dis[row - 3][col - 3] + 1

        else:
            dis[row, col] = np.min([dis[row, col - 1] + 1,  # левый
                                    dis[row - 1, col - 1] + __dist_matrix__[a[row-1]][b[col-1]],  # диаг      
                                    dis[row - 1, col] + 1])  # верхний

        col += 1
        i += 1
        if col == len(b) + 1:
            col = 0
            row += 1

    return dis[len(a), len(b)]

	
def phonetic_distance(word1, word2, stresses=False, transcription=False):
    
    """
    Расстояние между двумя словами на русском языке.
    Если варинатов транскрипции больше одного - выводятся все вохможные варианты.
    Если параметр transcription == True, будут выведены еще и сам разбор слов.
	
    >>> phonetic_distance('ехать', 'съехать', transcription=True)
    [['jехът’', 'сjехът’', 1.0]]
	
    >>> phonetic_distance('замок', 'замер', transcription=True)
    [['замък', 'зам’ьр', 0.6416666666666666],
    ['замък', 'зам’ер', 0.7666666666666666],
    ['замок', 'зам’ьр', 0.8916666666666666],
    ['замок', 'зам’ер', 0.7666666666666666]]
 	
    >>> phonetic_distance('замок', 'замок')
    [0.0, 0.25, 0.25, 0.0]

    """

    if not isinstance(word1, str) or not isinstance(word2, str):
        raise ValueError('Wrong data type')
    
    if word1 == '':
        return len(word2)
    
    if word2 == '':
        return len(word1)

    if stresses:

        if not isinstance(stresses, list):
            raise ValueError('Wrong data type')

        if len(stresses) != 2:
            raise ValueError('The number of stresses must be the same as the number of words')

        if not all(isinstance(x, int) for x in stresses):
            raise ValaueError('The stress values type must be int')

        word1 = phrase_transformer(word1, stresses=[(stresses[0])])
        word2 = phrase_transformer(word2, stresses=[(stresses[1])])

    else:
        word1 = phrase_transformer(word1)
        word2 = phrase_transformer(word2)

    if len(word1[0]) > 1:
        raise ValueError('Enter values must be words, not phrases')

    if len(word1[0]) > 1:
        raise ValueError('Enter values must be words, not phrases')

    answer = []

    for w1 in word1:
        for w2 in word2:

            if transcription:
                answer.append([''.join(w1[0]), ''.join(w2[0]), __lev_distance__(w1[0], w2[0])])
            else:
                answer.append(__lev_distance__(w1[0], w2[0]))

    return answer
