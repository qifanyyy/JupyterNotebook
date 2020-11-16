from fst import FST
import string, sys
from fsmutils import composechars, trace


def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """
    pop_letters_list = ['a','e','h','i','o','u','w','y']
    bfpv = ['b','f','p','v']
    cgjk = ['c','g','j','k','q','s','x','z']
    dt = ['d','t']
    l = ['l']
    mn = ['m','n']
    r = ['r']

    # Let's define our first FST
    f1 = FST('soundex-generate')


    f1.add_state('start')
    f1.add_state('one')
    f1.add_state('two')
    f1.add_state('three')
    f1.add_state('four')
    f1.add_state('five')
    f1.add_state('six')
    f1.add_state('seven')


    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('one')
    f1.set_final('two')
    f1.set_final('three')
    f1.set_final('four')
    f1.set_final('five')
    f1.set_final('six')
    f1.set_final('seven')


    # Add the rest of the arcs

    for letter in string.ascii_letters:
        if letter.lower() in bfpv:
            f1.add_arc('start','two',(letter),(letter))
        elif letter.lower() in cgjk:
            f1.add_arc('start','three',(letter),(letter))
        elif letter.lower() in dt:
            f1.add_arc('start', 'four', (letter), (letter))
        elif letter.lower() in l:
            f1.add_arc('start', 'five', (letter), (letter))
        elif letter.lower() in mn:
            f1.add_arc('start', 'six', (letter), (letter))
        elif letter.lower() in r:
            f1.add_arc('start', 'seven', (letter), (letter))
        else:
            f1.add_arc('start', 'one', (letter), (letter))
        if letter.lower() in pop_letters_list:
            f1.add_arc('one', 'one', (letter), ())
            f1.add_arc('two', 'one', (letter), ())
            f1.add_arc('three', 'one', (letter), ())
            f1.add_arc('four', 'one', (letter), ())
            f1.add_arc('five', 'one', (letter), ())
            f1.add_arc('six', 'one', (letter), ())
            f1.add_arc('seven', 'one', (letter), ())

        elif letter.lower() in bfpv:
            f1.add_arc('two', 'two', (letter), ())
            f1.add_arc('one', 'two', (letter), ('1'))
            f1.add_arc('three', 'two', (letter), ('1'))
            f1.add_arc('four', 'two', (letter), ('1'))
            f1.add_arc('five', 'two', (letter), ('1'))
            f1.add_arc('six', 'two', (letter), ('1'))
            f1.add_arc('seven', 'two', (letter), ('1'))

        elif letter.lower() in cgjk:
            f1.add_arc('three', 'three', (letter), ())
            f1.add_arc('one', 'three', (letter), ('2'))
            f1.add_arc('two', 'three', (letter), ('2'))
            f1.add_arc('four', 'three', (letter), ('2'))
            f1.add_arc('five', 'three', (letter), ('2'))
            f1.add_arc('six', 'three', (letter), ('2'))
            f1.add_arc('seven', 'three', (letter), ('2'))

        elif letter.lower() in dt:
            f1.add_arc('four', 'four', (letter), ())
            f1.add_arc('one', 'four', (letter), ('3'))
            f1.add_arc('three', 'four', (letter), ('3'))
            f1.add_arc('two', 'four', (letter), ('3'))
            f1.add_arc('five', 'four', (letter), ('3'))
            f1.add_arc('six', 'four', (letter), ('3'))
            f1.add_arc('seven', 'four', (letter), ('3'))

        elif letter.lower() in l:
            f1.add_arc('five', 'five', (letter), ())
            f1.add_arc('four', 'five', (letter), ('4'))
            f1.add_arc('one', 'five', (letter), ('4'))
            f1.add_arc('two', 'five', (letter), ('4'))
            f1.add_arc('three', 'five', (letter), ('4'))
            f1.add_arc('six', 'five', (letter), ('4'))
            f1.add_arc('seven', 'five', (letter), ('4'))

        elif letter.lower() in mn:
            f1.add_arc('six', 'six', (letter), ())
            f1.add_arc('five', 'six', (letter), ('5'))
            f1.add_arc('one', 'six', (letter), ('5'))
            f1.add_arc('two', 'six', (letter), ('5'))
            f1.add_arc('three', 'six', (letter), ('5'))
            f1.add_arc('four', 'six', (letter), ('5'))
            f1.add_arc('seven', 'six', (letter), ('5'))

        elif letter.lower() in r:
            f1.add_arc('seven', 'seven', (letter), ())
            f1.add_arc('six', 'seven', (letter), ('6'))
            f1.add_arc('one', 'seven', (letter), ('6'))
            f1.add_arc('two', 'seven', (letter), ('6'))
            f1.add_arc('three', 'seven', (letter), ('6'))
            f1.add_arc('four', 'seven', (letter), ('6'))
            f1.add_arc('five', 'seven', (letter), ('6'))
            f1.add_arc('six', 'seven', (letter), ('6'))

    return f1




def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.add_state('a')
    f2.add_state('b')
    f2.add_state('c')
    f2.add_state('2')

    f2.initial_state = '1'
    f2.set_final('1')
    f2.set_final('a')
    f2.set_final('b')
    f2.set_final('c')
    f2.set_final('2')

    # Add the arcs

    for letter in string.letters:
        f2.add_arc('1', '1', (letter), (letter))

    for n in range(10):
        f2.add_arc('1', 'a', (str(n)), (str(n)))
        f2.add_arc('a', 'b', (str(n)), (str(n)))
        f2.add_arc('b', '2', (str(n)), (str(n)))
        f2.add_arc('2', '2', (str(n)), ())

    return f2



def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    #f3.add_state('a1')
    f3.add_state('a')
    f3.add_state('b')
    f3.add_state('2')
    
    f3.initial_state = '1'
    f3.set_final('2')

    for letter in string.ascii_letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', 'a', (str(number)), (str(number)))
        f3.add_arc('a', 'b', (str(number)), (str(number)))
        f3.add_arc('b', '2', (str(number)), (str(number)))

    f3.add_arc('1', '2', (), ('000'))
    f3.add_arc('a', '2', (), ('00'))
    f3.add_arc('b', '2', (), ('0'))
    return f3

    # The above code adds zeroes

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))