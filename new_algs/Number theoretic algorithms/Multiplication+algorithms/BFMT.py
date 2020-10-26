from suffix_tree import Tree
import glob
import pandas as pd

INPUT = './text_data/training.1600000.processed.noemoticon.csv'
N_DOCS = 2500

# From https://stackoverflow.com/questions/35672809/how-to-read-a-list-of-txt-files-in-a-folder-in-python
def read_first_line(file):
    """Gets the first line from a file.

    Returns
    -------
    str
        the first line text of the input file
    """
    with open(file, 'rt') as fd:
        first_line = fd.readline()
    return first_line

def merge_per_folder(folder_path, output_filename):
    """Merges first lines of text files in one folder, and
    writes combined lines into new output file

    Parameters
    ----------
    folder_path : str
        String representation of the folder path containing the text files.
    output_filename : str
        Name of the output file the merged lines will be written to.
    """
    # make sure there's a slash to the folder path 
    folder_path += "" if folder_path[-1] == "/" else "/"
    # get all text files
    txt_files = glob.glob(folder_path + "*.txt")
    # get first lines; map to each text file (sorted)
    output_strings = map(read_first_line, sorted(txt_files))
    output_content = "".join(output_strings)
    # write to file
    return output_content

def get_BFMT(file=INPUT, n_docs=N_DOCS):
    docs = pd.read_csv(file, header=None, engine='python', nrows=n_docs)[5]
    docs = docs.apply(lambda x: x.lower())
    docs = docs.apply(lambda x: ''.join([i if ord(i) < 128 else ' ' for i in x]))
    docs = list(docs)
    tree = Tree(dict(enumerate(docs)))
    return tree, docs
