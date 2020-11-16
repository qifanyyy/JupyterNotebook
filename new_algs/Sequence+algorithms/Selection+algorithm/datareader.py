'''
Helper class for parsing input data and generating train/test sets.
Author: Tushar Makkar <tusharmakkar08[at]gmail.com>
Date: 17.11.2014
'''
import csv, numpy, random

def randomize_inputs(X, y):
    ''' 
    Randomizes the input samples, 
	just in case they are neatly ordered in the raw form.
    
    Args:
        X: data samples
        y: outputs for the data samples in X
        
    Returns:
        The shuffled input data samples.
    '''
    sequence = range(len(y))
    random.shuffle(sequence)
    new_X = []
    new_y = []
    for i in sequence:
        new_X.append(X[i])
        new_y.append(y[i])
    return (new_X, new_y)
 
def parse_input_no_conversion (input_file, custom_delimiter,
					 input_columns, output_column, is_test):
    ''' 
    This function parses the input data file, 
	performing no conversion on the input values.
    
    Args:
        input_file: The file containing the input data.
        custom_delimiter: The delimiter used in the input files.
        input_columns: Which columns in the input data are inputs (X). 
		If input_columns is empty, the data samples 
		have variable length.
        output_column: Which column in the input data is output 
		value (y).
        is_test: Set to True if we are parsing input from a test set.
    
    Returns:
        A set (X, y) containing the input data.    
    '''
    data_reader = csv.reader(open(input_file, 'rb'), 
						delimiter=custom_delimiter)
    if not is_test:
        X = []
        y = []
        for row in data_reader:
            line_x = [1] # Add the X0=1
            while '' in row:
                row.remove("")
            if input_columns != []:
                for i in input_columns:
                    if i < len(row):
                        line_x.append(row[i])
                X.append(line_x)
                y.append(row[output_column])
            else:
                for i in range(len(row)):
                    line_x.append(row[i])
                X.append(line_x)
                print (X)
        
        (X, y) = randomize_inputs(X, y)
    else:
        X = []
        for row in data_reader:
            line_x = [1]
            for i in range(len(row)):
                line_x.append(row[i])
            X.append(line_x)
        
        y = [0.0] * len(X) # Dummy y
        (X, y) = randomize_inputs(X, y)
    
    return (X, y)

def parse_input(input_file, custom_delimiter, input_columns, 
				output_column, is_test, input_literal_columns, 
				input_label_mapping, output_literal,
				output_label_mapping):
    ''' 
    This function parses the input data file and converts 
    literal values using the specified mappings.
    
    Args:
        input_file: The file containing the input data.
        custom_delimiter: The delimiter used in the input files.
        input_columns: Which columns in the input data are inputs (X). 
        If input_columns is empty, the data samples have variable length
        output_column: Which column in the input data is output 
        value (y).
        is_test: Set to True if we are parsing input from a test set.
        input_literal_columns: Which columns in the input data 
        have a literal description and need to be mapped to custom 
        numeric values.
        input_label_mapping: Mapping for input literal columns.
        output_literal: Boolean, shows whether output is literal 
        or numeric.
        output_label_mapping: Mapping for output literal column.
    
    Returns:
        A set (X, y) containing the input data.    
    '''
    data_reader = csv.reader(open(input_file, 'rb'), 
					delimiter=custom_delimiter)
    
    if not is_test:
        X = []
        y = []
        index = 0
        for row in data_reader:
            line_x = [1] # Add the X0=1
            while '' in row:
                row.remove("")
            if input_columns != []:
                for i in input_columns:
                    if input_literal_columns[i] == 1:
                        line_x.append(float(
						input_label_mapping[i][row[i]]))
                    else:
                        line_x.append(float(row[i]))
                X.append(line_x)
                if output_literal:
                    y.append(float(output_label_mapping[
						row[output_column]]))
                else:
                    y.append(float(row[output_column]))
            else:
                for i in range(len(row)):
                    line_x.append(float(row[i]))
                X.append(line_x)
        
        (X, y) = randomize_inputs(X, y)
    else:
        X = []
        for row in data_reader:
            line_x = [1]
            for i in range(len(row)):
                line_x.append(float(row[i]))
            X.append(line_x)
        
        y = [0.0] * len(X) # Dummy y
        (X, y) = randomize_inputs(X, y)
    
    return (X, y)

def readInputData(input_file, input_test_file, 
	convert_literals, custom_delimiter, proportion_factor, split, 
	input_columns, output_column, input_literal_columns, 
	input_label_mapping, output_literal, output_label_mapping):
    '''
    Main method for parsing the input data. The input data is 
    expected in CSV format, with a delimiter that can be 
    specified as parameter.
    The method generates a random permutation of the
    read data to be safe in case the original raw data is nicely ordered
    It uses the proportion_factor to determine how much data should be 
    for training and how much for testing.
    
    Args:
        input_file: The file containing the input data.
        input_test_file: The file containing the test data 
        (if applicable).
        convert_literals: If True, the literals in the input files 
        will be converted to numeric values as per the given mappings.
        custom_delimiter: The delimiter used in the input files.
        proportion_factor: If there is no special input_test_file, 
        a percentage of proportion_factor% from the input_file will be 
        used as test data. The samples are randomly selected.
        split: If true, the test data will be taken from input_file. 
        Otherwise, from input_test_file.
        input_columns: Which columns in the input data are inputs (X).
        output_column: Which column in the input data is output value 
        (y).
        input_literal_columns: Which columns in the input data have a 
        literal description and need to be mapped to 
        custom numeric values.
        input_label_mapping: Mapping for input literal columns.
        output_literal: Boolean, shows whether output is literal or 
        numeric.
        output_label_mapping: Mapping for output literal column.
    
    Returns:
        A set (train_X, train_y, test_X, test_y) containing training 
        data and test data. The test_y array contains dummy values.
    '''
    if convert_literals:
        (X, y) = parse_input(input_file, custom_delimiter, 
        input_columns, output_column, False, input_literal_columns, 
        input_label_mapping, output_literal, output_label_mapping)
    else:
        (X, y) = parse_input_no_conversion(input_file, custom_delimiter,
         input_columns, output_column, False)
    
    if split:
        splice_index = int(len(y) * proportion_factor)
        train_X = X[splice_index:]
        train_y = y[splice_index:]
        test_X = X[:splice_index]
        test_y = y[:splice_index]
        if convert_literals:
            return (numpy.array(train_X), numpy.array(train_y), 
            numpy.array(test_X), numpy.array(test_y))
        else:
            return (train_X, train_y, test_X, test_y)
    else: 
		# Take test values from input_test_file -- we assume same 
		# format as input_file!
        (test_X, test_y) = parse_input(input_test_file,
         custom_delimiter, input_columns, output_column, True, 
         input_literal_columns, input_label_mapping, output_literal, 
         output_label_mapping)
        if convert_literals:
            return (numpy.array(X), numpy.array(y), numpy.array(test_X),
             numpy.array(test_y))
        else:
            return (X, y, test_X, test_y)
