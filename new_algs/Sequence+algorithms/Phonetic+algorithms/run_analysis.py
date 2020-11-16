from analyse import *
import sys

CLEAR_CACHE = False
BACKUP_CACHE = True

def run(nG, nT, nD, mD, mG, mT):
    param = {'NGram distance': nG, 'NGram threshold': nT, 'Neighborhood distance': nD,'Metaphone neighbors': mD,
                                   'Metaphone nGrams': mG, 'Metaphone nG threshold': mT}



    analyse(param)




if __name__=='__main__':

    run(1,1,1,1,1,1)