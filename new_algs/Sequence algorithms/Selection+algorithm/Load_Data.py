import pandas as pd
import csv

def read_data():
    dataset = []
    # Every 10 lines are one row in the data table
    dataset_row = []
    for location in ['cleveland.data', 'hungarian.data', 'switzerland.data', 'long-beach-va.data']:
        with open(location) as file:
            reader = csv.reader((x.replace('\0', '') for x in file), delimiter=' ')
            for line in reader:
                #delete name field
                if ("name" in line):
                    del line[4]
                    line = [float(i) for i in line]
                    dataset_row += line
                    dataset.append(dataset_row)
                    dataset_row= []
                else:
                    line = [float(i) for i in line]
                    dataset_row += line

    # columns of the dataset
    column_names = ["ID", "SSN", "age", "sex", "painloc", "painexer", "relrest", "pncaden",
    "CP", "trestbps", "htn", "chol", "smoke", "cigs", "years", "FBS", "DM", "famhist",
    "restecg", "ekgmo", "ekgday", "ekgyr", "dig", "prop", "nitr", "pro", "diuretic", "proto",
    "thaldur", "thaltime", "met", "thalach", "thalrest", "tpeakbps", "tpeakbpd", "dummy", "trestbpd",
    "exang", "xhypo", "oldpeak", "slope", "rldv5", "rldv5e", "ca", "restckm", "exerckm",
    "restef", "restwm", "exeref", "exerwm", "thal", "thalsev", "thalpul", "earlobe",
    "cmo", "cday", "cyr", "num", "lmt", "ladprox", "laddist", "diag", "cxmain", "ramus",
    "om1", "om2", "rcaprox", "rcadist", "lvx1", "lvx2", "lvx3", "lvx4", "lvf", "cathef",
    "junk"]

    df = pd.DataFrame(dataset, columns=column_names)

    # Now get rid of all the columns that have the description "not used" in the
    # data description
    df = df.drop(columns = ["thalsev", "thalpul", "earlobe", "lvx1", "lvx2"])
    df = df.drop(columns = ["lvx3", "lvx4", "lvf", "cathef", "junk"])

    # Get rid of ID number, SSN, dummy column
    df = df.drop(columns = ["ID", "SSN", "dummy"])

    # Get rid of columns that have the description "irrelevant" in the data description
    df = df.drop(columns = ["restckm", "exerckm"])


    # 1, 2, 3, 4 in the num column all represent sick
    # Combine so that its just 1 represents sick
    y = df["num"].values
    y_updated = []
    for val in y:
        if (val == 2 or val == 3 or val == 4):
            y_updated.append(1)
        else:
            y_updated.append(val)

    df = df.drop(columns = ["num"])
    df["num"] = y_updated

    return df

# For now, just delete the rows that contain a nan
def clean_data(dataset):
    dataset = dataset.dropna()
    # dataset = dataset.interpolate(method='linear')
    return(dataset)
