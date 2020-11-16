from munkres import Munkres
from data import Data
import xlwt, xlrd
import os, logging, argparse, time

def solve(data):
    """Applies the Hungarian algorithm to the data."""
    start = time.clock() # Start timer
    m = Munkres()
    rm = data.rank_matrix
    logging.info("Solving...")
    indexes = m.compute(rm)
    end = time.clock() # Stop timer
    print ('--> Time elapsed: %f' % (end - start))
    
    solution = []
    total = 0
    i = 0
    logging.debug("Solution:")
    for row, column in indexes:
        value = rm[row][column]
        solution.append([data.names[row], data.col_to_sem(column), value])
        total += value
        logging.debug(' (%d) %s -> %s', value, solution[i][0], solution[i][1])
        i += 1 
    print ('--> Total cost: %d' % total)
    return (solution, total)

def main(args):
    filename = os.path.basename(args.filename)
    # Read XLS into Data object
    wb = xlrd.open_workbook(args.filename)
    ws = wb.sheet_by_index(0)
    # Get seminar list
    seminar_list = [str(seminar) for seminar in ws.row_values(1, start_colx=9, end_colx=None)]
    # Get number of students and seminars
    num_students = ws.nrows - 2
    num_seminars = len(seminar_list)
    # Get ranking matrix
    rank_matrix = []
    for i in range(num_students):
        rank_row = [100 if c=='' else int(c) for c in ws.row_values(i+2, start_colx=
                9, end_colx=None)]
        rank_matrix.append(rank_row)

    # Create a Data object and apply the hungarian algorithm
    data = Data(rank_matrix, seminar_list)
    (solution, cost) = solve(data)
    
    # Initialize the Excel workbook and sheet
    sb = xlwt.Workbook(encoding = "utf-8")
    s1 = sb.add_sheet("Results")

    s1.write(0, 0, "Student")
    s1.write(0, 1, "Seminar")
    s1.write(0, 2, "Original Ranking")
    s1.write(0, 3, "Minimum Cost")
    s1.write(1, 3, cost)

    for i in range(len(solution)):
        s1.write(i+1,0,solution[i][0])
        s1.write(i+1,1,solution[i][1])
        s1.write(i+1,2,solution[i][2])

    result_filename = os.path.splitext(filename)[0]+"_results.xls"
    result_path = os.path.join("results", result_filename)
    sb.save(result_path)
    print ("Results saved to " + result_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug',
        help    = 'Print lots of debugging statements',
        action  = "store_const",
        dest    = "loglevel",
        const   = logging.DEBUG,
        default = logging.WARNING
    )
    parser.add_argument('-v','--verbose',
        help   = 'Be verbose',
        action = "store_const",
        dest   = "loglevel",
        const  = logging.INFO
    )
    parser.add_argument('filename', help="Path to survey response .xls")
    args = parser.parse_args()    
    
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='    %(message)s', level=args.loglevel)

    main(args)
