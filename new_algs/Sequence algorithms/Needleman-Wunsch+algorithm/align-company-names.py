import pandas as pd
import numpy as np
import time
import string
import regex
import argparse
from NW_Company_Names.NW_company_names import create_nw_df 

# Arg parsing
parser = argparse.ArgumentParser(description="Match sequences of company names.")
parser.add_argument("index_csv", type = argparse.FileType("r"), help = "CSV with index name data")
parser.add_argument("book_csv", type = argparse.FileType("r"), help = "CSV with company name data")
parser.add_argument("output_csv", type = argparse.FileType("w"), help = "Output name")
parser.add_argument("--nrows", type = int, help = "nrow to use", default=None)
parser.add_argument("--gap_penalty", type = float, help = "gap penalty size", default=-1)
parser.add_argument("--index_col", type = str, help = "index text column name", default="index_text")
parser.add_argument("--book_col", type = str, help = "book text column name", default="book_text")
parser.add_argument("--data_source_type", type = str, help = "Firm type used in PR (bank, credit union, etc.)", default=None)

def NW_align_names(index_csv,
                   book_csv,
                   output_csv,
                   index_col,
                   book_col,
                   data_source_type = None,
                   nrows = None,
                   gap_penalty = -1):
    """
    Aligns two sequences of company names using edit distance as a cost metric and the
    Needleman-Wunsch .algorithm
    
    Arguments:
        index_csv {str} -- csv with index names - must be labelled "text". 
        book_csv {str}         -- csv with book names - must be labelled "company name"
        output_csv {str} -- Output csv path

    Keyword Arguments:
        index, bank, supplement etc.) (default: {"firm"})
        nrows {int} -- Number of rows to use, defaults to None.
        gap_penalty {float} How large to penalise the algorithm for introducing a gap.
    
    
    Returns:
        [Pandas DataFrame] -- Pandas DF with matched sequences and respective
        indices. sequence_text_x is the book and sequence_text_y the index
    """
    index_df = pd.read_csv(index_csv,   nrows = nrows)
    book_df = pd.read_csv(book_csv, nrows = nrows)    
    
    
    # Since Personnel Records uses data source type to split up sections of the book
    # we don't want to match credit_union firms to bank firms.
    # Might be nicer to refactor this or split data in R before it reaches this stage
    if data_source_type != None:
        index_df = index_df[index_df["data_source_type"] == data_source_type]
        book_df = book_df[book_df["companyid"].str.contains(data_source_type)]
        # Again this is ugly and should be done elsewhere.
        # We want to ensure company names are ordered sequentially as they appear
        # in the book - as long as companyid is ZERO PADDED this will order entries

        # This should be the case for 54 (and hopefully 56) but here's a quick doublecheck
        book_df = book_df.sort_values(by = ["companyid"])


    subset_index_df = index_df.reset_index()
    subset_book_df = book_df.reset_index()

    # Removing digits
    subset_index_df["clean_index_text"] = subset_index_df[index_col].str.replace(r"\d+", "")
    # Removing Latin Characters
    subset_index_df["clean_index_text"] = subset_index_df["clean_index_text"].apply(lambda x: regex.sub(r"\p{Latin}", u"", str(x)))
    # Removing punctuation
    subset_index_df["clean_index_text"] = subset_index_df["clean_index_text"].apply(lambda x: regex.sub(r"\p{Punct}", u"", str(x)))
    subset_index_df["clean_index_text"] = subset_index_df["clean_index_text"].apply(lambda x: regex.sub(r"\|", u"", str(x)))
    
    # Run algo
    matched_df =  create_nw_df(
        subset_book_df,
        subset_index_df,
        book_col,
        "clean_index_text",
        gap_penalty = gap_penalty 
        )
    matched_df.to_csv(output_csv)
    return matched_df


if __name__ == "__main__":
    args = parser.parse_args()
    # Timing
    start = time.time()
    init_df = NW_align_names(
        args.index_csv,
        args.book_csv,
        args.output_csv,
        index_col = args.index_col,
        book_col = args.book_col,
        data_source_type = args.data_source_type,
        nrows = args.nrows,
        gap_penalty = args.gap_penalty
    )
    end = time.time()
print(init_df[["sequence_1", "sequence_2", "sequence_text_x", "sequence_text_y"]])
print("Time Taken:", end - start)