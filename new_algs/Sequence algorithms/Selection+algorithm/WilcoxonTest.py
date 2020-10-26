'''
Helper class for checking whether 2 distributions are same or not
Author: Tushar Makkar <tusharmakkar08[at]gmail.com>
Date: 29.01.2015
'''

from scipy import stats
import mushrooms_bfgs

def WilcoxonTest(Original_input, Symbiotic_output, Modified_GA_output):
    '''
    Returns the most similar output to Original_input out of 
    Symbiotic_output and GA_output using Wilcoxon Rank Sum Test.
    Args:
        Original_input: Data with N features
        Symbiotic_output: Data with N-1 features extracted using 
                          symbiotic algorithm
        Modified_GA_output: Data with N-1 features extracted using 
                            Modified Genetic algorithm
    Returns:
        The best suited N-1 features for a given distribution or [-1]
    '''
    z_stat_for_symbiotic, p_val_for_symbiotic = stats.ranksums(
                            Symbiotic_output, Original_input)
    z_stat_for_GA, p_val_for_GA = stats.ranksums(
                            Modified_GA_output, Original_input)
    print p_val_for_symbiotic, p_val_for_GA
    if max(p_val_for_GA , p_val_for_symbiotic) < 1e-300:
        return -1
    if (p_val_for_GA > p_val_for_symbiotic): 
        print "Forest one is better"
        return 1
    else: 
        print "Symbiotic is better"
        return 0
        
if __name__ == '__main__':
    (train_X, train_y, test_X, test_y) = mushrooms_bfgs.initialize(float(80)/100)
    (train_X_Sym, test_X_Sym) = mushrooms_bfgs.featureRemoval(train_X, test_X, [3])
    (train_X_For, test_X_For) = mushrooms_bfgs.featureRemoval(train_X, test_X, [16])
    #~ print train_X[0], train_X_Sym[0], train_X_For[0]
    if WilcoxonTest(train_X.ravel(), train_X_Sym.ravel() ,train_X_For.ravel()):
        newData_Tr = train_X_For
        newData_Ts = test_X_For
    else:
        newData_Tr = train_X_Sym
        newData_Ts = test_X_Sym
    #~ print WilcoxonTest([1,2,3,4], [1,2,3,5],[0,9,10,11])
