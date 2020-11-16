'''
Created on 16-Nov-2013

@author: Meghana M Reddy
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD 



def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    matrix_vec_val = []
    sparse_val = []
    sparse_ind = []

    for idx , i in enumerate(vector_list):
        matrix_val = []
        for j in range(0 , len(i)):
            columns = len(i)
            matrix_val.append(i[j])
        
        if(i.is_zero() == False):
            
            sparse_val.append(i)
            sparse_ind.append(idx)
        
        matrix_vec_val.append(make_vector(matrix_val , lambda x : (x == 0)))
            
    if float(len(sparse_val))/float(len(vector_list)) < DENSITY_THRESHOLD and float(len(vector_list) * columns) > SIZE_THRESHOLD:
        obj = SparseMatrix(sparse_val , sparse_ind , len(vector_list),columns)
    else :
        obj = FullMatrix(matrix_vec_val)
         
    return obj



org_rows = 0
org_column = 0
flag = 0
rows = 0
columns = 0



def pad_zeros(num):
    
    import math
    root = math.pow(num , 0.5)
    power = math.ceil(root)
    pad_zeros = 2**power - num
    return pad_zeros



def padding (self):
    
    list_vectors = []
    global org_rows , org_column
    org_rows = len(self)
    org_column = len(self[0])
    
    pad_zeros_rows = pad_zeros(len(self[0]))
    pad_zeros_column = pad_zeros(len(self))
    dimen = max(int(pad_zeros_rows) + len(self[0]) , int(pad_zeros_column) + len(self))
    
    for i in range(0 , len(self)):
        padded_row = self[i] + [0]*(dimen - len(self[i]))
        vec = make_vector(padded_row , lambda x : (x == 0))
        list_vectors.append(vec)
    lst = [0]*(dimen)

    for i in range(0 , (dimen-len(self))):
        vec = make_vector(lst , lambda x : (x == 0))
        list_vectors.append(vec)
   
    return make_matrix(list_vectors)



def unpadding(self):
    
    global org_rows , org_column
    unpadded_list = []
    
    for i in range(0 , org_rows):
        lst = []
        for j in range(0 , org_column):
            lst.append(self[i][j])
        vec = make_vector(lst , lambda x : (x == 0))
        unpadded_list.append(vec)
    
    return make_matrix(unpadded_list)
        
    
    
class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 5

    def __init__(self, rows):
        '''
        'rows' is a list of vectors
        Keep this is the row list for the matrix
        '''
       
        self.rows = rows



    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        
        return len(self.rows)


    
    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        
        if attr == 'nrows':
            return len(self.rows)
        
        if attr == 'ncolumns':
            return len(self.rows[0])
        
        
    
    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        
        
        if(isinstance(key,int)):
            lst = []
            for i in range(0,len(self.rows[key])):
                lst.append(self.rows[key][i])
            return lst
        
        else:
            return self.rows[key[0]][key[1]]
        
        
         
    
    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        
        
        if len(self) <= self.MIN_RECURSION_DIM :
            return True
        
        return False
            

    
    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        
    
        matrix_sum = []
        if len(self) != len(mat) :
            return None
        
        for i in range(0 , len(self)):
            v1 = make_vector(self[i] , lambda x : (x == 0))
            v2 = make_vector(mat[i] , lambda x : (x == 0))
            matrix_sum.append(v1 + v2)
        
        return make_matrix(matrix_sum)

    
    
    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        matrix_diff = []
        if len(self) != len(mat) :
            return None
        
        for i in range(0 , len(self)):
            v1 = make_vector(self[i] , lambda x : (x == 0))
            v2 = make_vector(mat[i] , lambda x : (x == 0))
            matrix_diff.append(v1 - v2)
        
        return make_matrix(matrix_diff)
        
        
        
    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        
        lst_iadd = []
        for i in range(0 , min(len(self) , len(mat))):
            v1 = make_vector(self[i] , lambda x : (x == 0))
            v2 = make_vector(mat[i] , lambda x : (x == 0))
            v1 += v2
            lst_iadd.append(v1)
        
        return make_matrix(lst_iadd)
        


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        lst_isub = []
        
        for i in range(0 , min(len(self) , len(mat))):
            v1 = make_vector(self[i] , lambda x : (x == 0))
            v2 = make_vector(mat[i] , lambda x : (x == 0))
            v1 -= v2
            lst_isub.append(v1)
        
        return make_matrix(lst_isub)



    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        
        left_matrix = []
        right_matrix = []
        
        for i in range(0 , len(self)):
            vec = make_vector(self[i]  ,lambda x : (x == 0))
            left_vector , right_vector = vec.split()
            left_matrix.append(left_vector)
            right_matrix.append(right_vector)
        
        return make_matrix(left_matrix),make_matrix(right_matrix )
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        
        left_matrix , right_matrix = self.left_right_split()
        
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []
        
        
        mid = len(left_matrix) / 2
        for i in range(0 , mid):
            topleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
            
        mid = len(right_matrix) / 2
        for i in range(0 , mid):
            topright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
            
        return make_matrix(topleft) , make_matrix(topright) , make_matrix(bottomleft) , make_matrix(bottomright)
            
        
        
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        
        if(len(self) != len(mat)):
            return None
        
        merged_list= []
        for i in range(0 , len(self)):
            vec = make_vector(self[i]  , lambda x : (x == 0))
            vec.merge(mat[i])
            merged_list.append(vec)
        
        return make_matrix(merged_list )




    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        
        final_list = []
        for i in range(0 , len(self)):
            vec = make_vector(self[i]  , lambda x : (x == 0))
            final_list.append(vec)
        
        
        for i in range(0 , len(mat)):
            vec = make_vector(mat[i]  , lambda x : (x == 0))
            final_list.append(vec)
        
        return make_matrix(final_list)
    
    
    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        
        rmul_vector = []
        for i in range(0 , len(self)):
            Sum = 0
            for j in range(0 , len(vec)):
                Sum = Sum + vec[j] * self[j][i]
            rmul_vector.append(Sum)
          
        return make_vector(rmul_vector , lambda x : (x == 0))

    
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
       
        if(len(self[0]) != len(mat)):
            print ("INCOMPATIBLE MULTIPLICATION")
            return
        else:
            if(self.is_small() == True or mat.is_small() == True):
                lst_mul = []
                
                for i in range(0 , len(self)):
                    vec = make_vector(self[i] , lambda x : (x == 0))
                    vec_mul = mat.rmul(vec)
                    lst_mul.append(vec_mul)
                
                return make_matrix(lst_mul)
            
            global flag
            if(flag == 0):
                global rows , columns
                flag = 1
                self = padding(self)
                mat = padding(mat)
                if(len(self) != len(mat)):
                    minimum = min(len(self) , len(mat))
               
                    if(minimum == len(self)):
                        matrix = self
                    else:
                        matrix = mat
                    
                    lst_vec = []
                    pad = abs(len(self) - len(mat))
                  
                    for i in range(0,len(matrix)):
                        pad_row = matrix[i] + [0] * pad
                        vec = make_vector(pad_row , lambda x : (x == 0))
                        lst_vec.append(vec)
                    
                    for i in range(0,pad):
                        pad_row = [0]*len(mat)
                        vec = make_vector(pad_row , lambda x : (x == 0))
                        lst_vec.append(vec)
                    
                    matrix = make_matrix(lst_vec) 
                    
                    if(minimum == len(self)):
                        self = matrix
                    else:
                        mat = matrix
                    
                rows = len(self)
                columns = len(self[0])
                
            
            A , B , C , D = self.get_quarters()
            E , F , G , H = mat.get_quarters()
            
            P1 = (A + D) * (E + H)
            P2 = (C + D) * E
            P3 = A * (F - H)
            P4 = D * (G - E)
            P5 = (A + B) * H
            P6 = (C - A) * (E + F)
            P7 = (B - D) * (G + H)
            
            top_left =  P1 + P4 - P5 + P7
            top_right = P3 + P5
            bottom_left = P2 + P4
            bottom_right = P1 - P2 + P3 + P6
            
            x = top_left.merge_cols(top_right)
            y = bottom_left.merge_cols(bottom_right)
            
            final_mat = x.merge_rows(y)
        
            if(len(final_mat) == rows and len(final_mat[0]) == columns):
                final_mat = unpadding(final_mat)
            
            return final_mat
    
            
        
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        
        if(len(self) != len(mat)):
            return False
        
        for i in (0 , len(self)):
            for j in (0 , len(self)):
                if self[i][j] !=  mat[i][j] :
                    return False
        
        return True
    
    
            
class FullMatrix(Matrix):
    '''
    A subclass of Matrix where all rows (vectors) are kept explicitly as a list
    '''
    def __init__(self, vectors):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
        '''
        super(FullMatrix, self).__init__(vectors)
        self.vectors = vectors


class SparseMatrix(Matrix):
    '''
    A subclass of Matrix where most rows (vectors) are zero vectors
    The vectors (non-zero) and their corresponding indices are kept in separate lists
    '''
    def __init__(self, vectors, indices, length=0,column=0):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix , self).__init__(vectors)
        self.vectors = vectors
        self.indices = indices
        self.rows = length
        self.column = column
        

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return self.rows

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        if (isinstance(key , int)):
            if key in self.indices:
                lst = []
                for i in range(0 , self.column):
                    idx = bisect_left(self.indices,key)
                    lst.append(self.vectors[idx][i])
                return lst
            else:
                return [0]*self.column
        else:
            if key[0] in self.indices:
                idx = bisect_left(self.indices,key[0])
                return self.vectors[idx][key[1]]
            else:
                return 0
            
            
            
    def merge_rows(self , mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        if len(self) != len(mat):
            return None
        
        merged_list = []
        
        for i in range(0 ,len(self)):
            vec = make_vector(self[i] , lambda x : (x == 0))
            merged_list.append(vec)
        
        for i in range(0,len(mat)):
            vec = make_vector(mat[i], lambda x : (x == 0))
            merged_list.append(vec)
        
        return make_matrix(merged_list)

        

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        left_matrix , right_matrix = self.left_right_split()
        
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []
                        
        mid = len(left_matrix) / 2
        for i in range(0 , mid):
            topleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
            
        mid = len(right_matrix) / 2
        for i in range(0 , mid):
            topright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
            
        return make_matrix(topleft) , make_matrix(topright) , make_matrix(bottomleft) , make_matrix(bottomright)


v1 = make_vector([1,2,1,1,3,4,1,1] , lambda x : (x == 0))
v2 = make_vector([1,1,1,1,1,1] , lambda x : (x == 0))
v3 = make_vector([1,2,3,4,5] , lambda x : (x == 0))
v4 = make_vector([1,0,0,0,0,0,2,0,3,4,5,6] , lambda x : (x == 0))
v5 = make_vector([0,0,1,0,1,0,0,0,3,6,5,1] , lambda x : (x == 0))
v6 = make_vector([0,0,1,0,0,0,1,0,3,4,1,6] , lambda x : (x == 0))
v7 = make_vector([1,0,2,0] , lambda x : (x == 0))
v8 = make_vector([0,0,0,0] , lambda x : (x == 0))


m1 = make_matrix([v7,v8,v8,v8,v8,v8,v8,v8])
m2 = make_matrix([v8,v8,v8,v8])
print ("m1")
for i in range(0,len(m1)):
    for j in range(0,len(m1[i])):
        print (m1[i][j],)
    print() 
print ("m2")
for i in range(0,len(m2)):
    for j in range(0,len(m2[i])):
        print (m2[i][j],)
    print() 

print()
x  =  m2 * m2
for i in range(0,len(x)):
    for j in range(0,len(x[i])):
        print (x[i][j],)
    print()
print()
    
    
    

