import os
import pandas as pd

# target encoding
coding = 'utf-8'
# directory
file_dir = '/Users/linjliang/Learning/ML/CourseProject/News Video Story Segmentation/jsonresult/'

def run_coding():
    for root, dirs, files in os.walk(file_dir, topdown=False):
        for i in files:
            files_name = os.path.join(root, i)
            try:
                df1 = pd.read_csv(files_name, encoding='utf-8')
            except:
                df1 = pd.read_csv(files_name, encoding='gbk')
            df1.to_csv(files_name, encoding=coding,index=None)

if __name__ == '__main__':
    run_coding()
    print("It's done")