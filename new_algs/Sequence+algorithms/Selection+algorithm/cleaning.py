import pandas as pd

DISTRIBUTION_THRESHOLD = 10


def clean_df(df, y):
    rows, cols = df.shape
    columns = list(df.columns)
    columns.remove(y)

    for col in columns:
        df_dtype = df[col].dtype
        conti = check_if_conti(df[col], DISTRIBUTION_THRESHOLD)

        # if the column is a string column
        if df_dtype == 'O':

            # if the column has continious values, that column is removed
            if conti:
                print("Dropped the column "+ col)
                
            # if the column has classes, filled missing values with mode
            else:
                print("Filling column " + col + " with mode of the same column")
                df[col].fillna(df[col].mode()[0], inplace=True)

                dummies_df = pd.get_dummies(df[col])
                print("Dropping the column "+ col + " and creating dummy columns")
                df = pd.concat([df, dummies_df], axis = 1)
                
            df.drop([col], axis = 1, inplace = True)
        # if the column is a number column
        else:

            # if the column has continious distribution, filled missing values with mean
            if conti:
                print("Filling column " + col + " with mean of the same column")
                df[col].fillna((df[col].mean()), inplace=True)

            # if the column has classes, filled missing values with mode
            else:
                print("Filling column " + col + " with mode of the same column")
                df[col].fillna(df[col].mode()[0], inplace=True)
            
    return df


def check_if_conti(df_col, threshold):
    unique_values = len(df_col.unique())
    total_values = len(df_col)
    distribution = (unique_values / total_values) * 100

    if distribution > threshold:
        return True
    
    return False