# import for the CLI
import sys
import getopt
import os


# return a list of the following type:
# boolean, boolean, boolean, string
# representing the arguments {automatic, display_plot, save_plots, input_file}
# the default will be returned if no arguments is passed
#
#
# input_file arguments is mandatory
#
# Arguments:
# the defaults are taken from the main script, usually they are:
# nr_ind_start = 10
# nr_generations = 10
# environment = (400, 400)
# nat_selection = False
# d_analysis = False
# file_path = 'natural_selection_data.csv'
#
def get_arguments():
    # default settings
    nr_ind_start = 10
    nr_generations = 10
    genes = [-98, -69, -65, -46, 49, 50, 74, 91, 117, 178]
    length = 400
    width = 400
    nat_selection = False
    d_analysis = False
    d_analysis_option = ''
    file_path = ''

    full_cmd_arguments = sys.argv

    argument_list = full_cmd_arguments[1:]

    short_options = 'hp:g:l:w:na:f:'
    long_options = ['help', 'pop=', 'gen=', 'length=', 'width=', 'nat', 'analysis=', 'file=']

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)

    return_list = []
    # parse the arguments
    for current_argument, current_value in arguments:
        if current_argument in ('-h', '--help'):  # help argument is parsed and display information
            print('\n\nStart the program in the following order, where [-c] is optional')
            print('python Houses_prices.py [-p nr] [-g nr] [-l nr] [-w nr] [-n] [-a opt] -f location_input\n')
            print('-p / --pop           | set the initial population, default 10')
            print('-g / --gen           | set the number of generations, default 10')
            print('-l / --length        | set the environment length, default 400')
            print('-w / --width         | set the environment width, default 400')
            print('-n / --nat           | run the natural selection algorithm')
            print('-a / --analysis      | run the data analysis algorithm\n',
                  ' ' * 19, '| options:\n',
                  ' ' * 19, '| s -> save plots\n',
                  ' ' * 19, '| d -> display plots\n',
                  ' ' * 19, '| sd -> save and display plots')
            print('-f / --file          | input/output file of the data\n\n')
            exit(0)
        elif current_argument in ('-p', '--pop'):  # nr of start individual is set by user
            nr_ind_start = int(current_value)
        elif current_argument in ('-g', '--gen'):  # number of generations set by the user
            nr_generations = int(current_value)
        elif current_argument in ('-l', '--length'):  # environment length set by user
            length = int(current_value)
        elif current_argument in ('-w', '--width'):  # environment width set by user
            width = int(current_value)
        elif current_argument in ('-n', '--nat'):  # user argument is parsed and set the boolean variable
            nat_selection = True
        elif current_argument in ('-a', '--analysis'):  # user argument is parsed and set the boolean variable
            d_analysis = True
            d_analysis_option = current_value
            if d_analysis_option == 's' or d_analysis_option == 'sd':
                # create the folder if it doesn't exist
                if not os.path.exists('Images'):  # if the folder 'Images' doesn't exist, create one
                    os.makedirs('Images')
        elif current_argument in ('-f', '--file'):  # input path argument is parsed
            while file_path == '':  # while the input is null, search for it
                file_path = sys.argv[-1]
                if file_path[-4:] != '.csv':  # if the last 4 chars of the command are not good, raise error
                    file_path = ''
                    print('Wrong input, please see the -h/ --help information')
                    exit(0)
    if file_path == '':
        file_path = 'natural_selection_data.csv'
    return_list.append(nr_ind_start)
    return_list.append(nr_generations)
    return_list.append(genes)
    return_list.append((length, width))
    return_list.append(nat_selection)
    return_list.append(d_analysis)
    return_list.append(d_analysis_option)
    return_list.append(file_path)
    return return_list
