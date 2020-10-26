from Utils.file_loader import get_dataframes, get_generated_dataframes
from multiprocessing import Pool
from run_clustering import main as write_measures
import pandas as pd
import pickle
import os
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def main():
    dataframes = get_dataframes()
    generated_dfs = get_generated_dataframes()
    total_dfs = dataframes + generated_dfs
    final_results = []

    with Pool(8) as p:
        for x in p.map(write_measures, total_dfs):
            final_results.append(x)

    
    pickle.dump(final_results, open(os.path.join(os.getcwd(), 'results.pkl'), 'wb'))
    
    df = pd.DataFrame.from_records(final_results, columns=['dbscan', 'mst', 'SL', 'eac', 'khmeans', 'kmeans', 'psc', 'dataset'])
    df.to_csv('rankings.csv')

if __name__ == "__main__":
    main()