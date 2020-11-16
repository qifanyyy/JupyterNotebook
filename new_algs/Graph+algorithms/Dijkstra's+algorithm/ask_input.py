# ask_input.py
# Eric Du
# edu1@stu.parkland.edu
# CSC 220, Spring 2016
# Prompt question, accept input of certain type within min/max or range,
# and return input if valid

def ask_input(prompt, type_ = None, min_ = None, max_ = None, range_ = None):
    while True:
        i = input(prompt)
        if type_ is not None:
            try:
                i = type_(i)
            except ValueError:
                print("Input type must be", type_.__name__)
                continue
        if max_ is not None and i > max_:
            print("Input must be less than or equal to", max_)
        elif min_ is not None and i < min_:
            print("Input must be greater than or equal to", min_)
        elif range_ is not None and i not in range_:
            if isinstance(range_, range):
                print("Input must be between", range_.start, "and", 
                range_.stop)
            else:
                print("Input must be", range_)
        else:
            return i
