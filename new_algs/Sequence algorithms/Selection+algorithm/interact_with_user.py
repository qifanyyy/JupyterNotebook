import sqlite3
import numpy as np
import pandas as pd

# Connect to database
conn = sqlite3.connect("courses.db")
c = conn.cursor()

# Prepare table by deleting rows with missing data
statement = "delete from coursedata where {} or {} or {}"
statement = statement.format(
    "course_level = -1",
    "course_category = -1",
    "course_enrollment = -1"
)
conn.execute(statement)

data = pd.read_sql("select * from coursedata", con=conn)

# Figure out which dimension to present to the user
def which_col(data):
    results = []
    dim1 = data["course_level"]
    dim2 = data["course_category"]
    dim3 = data["course_enrollment"]

    if dim1.max() != dim1.min():
        result_1 = (dim1.max() - dim1.min()) / dim1.std()
        results.append((result_1, "course_level"))

    if dim2.max() != dim2.min():
        result_2 = (dim2.max() - dim2.min()) / dim2.std() 
        results.append((result_2, "course_category"))

    if dim3.max() != dim3.min():
        result_3 = (dim3.max() - dim3.min()) / dim3.std()
        results.append((result_3, "course_enrollment"))

    # return dimension with greatest standardized range
    max_result, max_dimension = max(results)
    return max_dimension 

def print_options(low, med, high):
    print("Here are three example courses:")    
    print(low[1])
    print("\tLevel:\t\t{}".format(low[2])) 
    print("\tCategory:\t{}".format(low[3])) 
    print("\tEnrollment:\t{}".format(low[4])) 
    print(med[1])
    print("\tLevel:\t\t{}".format(med[2])) 
    print("\tCategory:\t{}".format(med[3])) 
    print("\tEnrollment:\t{}".format(med[4])) 
    print(high[1])
    print("\tLevel:\t\t{}".format(high[2])) 
    print("\tCategory:\t{}".format(high[3])) 
    print("\tEnrollment:\t{}".format(high[4])) 

def parse(selection):
    if selection in ["1", "2", "3"]:
        return int(selection)
    else:
        return parse(input("Please enter 1, 2, or 3.\n"))

# Execute one iteration of our algorithm
def step(data):
    col = which_col(data)
    data.sort_values(by=col, inplace=True)
    print_options(
        data.iloc[0], 
        data.iloc[round(len(data)/2)], 
        data.iloc[-1]
    )
    print("Based on the dimension of " + col.split("_")[1] + ",")
    selection = parse(input("Do you prefer course 1, 2, or 3?\n"))
    segment_start = round((selection-1) * len(data)/3)
    segment_end = round(selection * len(data)/3)
    return data.iloc[segment_start:segment_end]

while len(data) > 6:
    print("__________________________________________")
    newdata = step(data)
    print("Your top courses are: ") 
    print(newdata.head())
    print("There are {} courses remaining.".format(len(newdata)))
    if len(newdata) < 3:
        print("Stopping execution because there are too few courses.")
        break
    data = newdata

# Close database connection without saving changes
conn.close()

# Try numpy, pandas, SQLite, SQLAlchemy and see which is faster