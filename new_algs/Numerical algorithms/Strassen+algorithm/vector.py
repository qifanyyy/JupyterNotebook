'''
Created on 16-Nov-2013

@author: Meghana M Reddy
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 5

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    count = 0
    for i in lst:
        if zero_test(i) :
            count = count + 1
    
    non_zeros = len(lst) - count
    
    if float(non_zeros)/float(len(lst)) < DENSITY_THRESHOLD and len(lst) > SIZE_THRESHOLD:
        return True
    else:
        return False
    
    
    
def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    if(is_long_and_sparse(data , zero_test)):
        list_values = []
        list_indices = []
        for idx , i in enumerate(data):
            if not(zero_test(i)) :
                list_values.append(i)
                list_indices.append(idx)
        
        vector = SparseVector(list_values , list_indices , len(data) , zero_test)
    else:
        vector = FullVector(data)
        
    return vector
        
    

class Vector(object):
    '''
    Base Vector class - implements a number of the common methods required for a Vector
    '''
    def __init__(self , lst , zero_test = lambda x : (x == 0)):
        '''
        Have a data attribute that is initialized to the list of elements given in the argument 'lst'
        zero_test is a function that tests if a given element is zero (remember you could potentially
        have a vector of complex numbers, even a vector of functions, ... not just numbers 
        '''
        
        self.data = lst
        self.zero_test = zero_test



    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        
        return (len(self.data))



    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        
        return self.data[i]
    
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        
        self.data[i] = val
        
            
    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        
        for i in self.data:
            if not(self.zero_test(i)):
                return False
        
        return True
        


    def components(self):
        '''
        Allows one to iterate through the elements of the vector as shown below
        for elem in vector.components(): (vector is an object of type Vector or any of its derived classes)
        '''
        
        for i in xrange(len(self)):
            yield self[i]



    def __eq__(self , vector):
        '''
        Check if this vector is identical to another 'vector' (allows use of operator == to compare vectors)
        '''
        
        for i in range(0 , len(self)):
            if(self[i] != vector[i]):
                return False
            
        return True
           
            
    
    def __mul__(self , vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        
        scalar_sum = 0
        
        if(len(vector) != len(self)):
            return None
        
        for i in range(0 , len(self)):
            scalar_sum = scalar_sum + vector[i] * self[i]
        
        return scalar_sum
            


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        sum_list = []
        
        if(len(vector) != len(self)):
            return None
        
        for i in range(0 , len(self)):
            sum_list.append (vector[i] + self[i])
        
        return make_vector(sum_list , self.zero_test)
        
        
    
    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
       
        sub_list = []
        
        if(len(vector) != len(self)):
            return None
        
        for i in range(0 , len(self)):
            sub_list.append (self[i] - vector[i] )
        
        return make_vector(sub_list , self.zero_test)

    
   
    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        for i in range(0 , min(len(self) , len(vector))):
            self[i] = self[i] + vector[i]
            
        return make_vector(self.data , self.zero_test)
        
        

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        for i in range(0 , min(len(self) , len(vector))):
            self[i] = self[i] - vector[i]

        return make_vector(self.data , self.zero_test)
        
    
    
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        length = len(self)
        mid = length/2
        first_half = []
        second_half = []
        
        for i in (0 , mid):
            first_half.append(self[i])
        
        for i in (mid , length):
            second_half.append(self[i])
        
        make_vector(first_half , self.zero_test)
        make_vector(second_half , self.zero_test)
        
        return first_half , second_half
        
        
        
class FullVector(Vector):
    '''
    A subclass of Vector where all elements are kept explicitly as a list
    '''
    def __init__(self , lst , zero_test = lambda x : (x == 0)):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
        '''
        super(FullVector, self).__init__(lst, zero_test)
        self.data = lst
        self.zero_test = zero_test

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        
        length = len(self)
        mid = length/2
        first_half = []
        second_half = []
        
        for i in range(0,mid):
            first_half.append(self[i])
        for i in range(mid,length):
            second_half.append(self[i])
        
        first_vect = make_vector(first_half , self.zero_test)
        second_vect = make_vector(second_half , self.zero_test)
        
        return first_vect , second_vect
        
       
        
    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        
        for i in vector:
            self.data.append(i)
            


class SparseVector(Vector):
    '''
    Vector that has very few non-zero entries
    Values and corresponding indices are kept in separate lists
    '''
    def __init__(self, values, indices, length = 0, zero_test = lambda x : (x == 0)):
        '''
        'values' argument is the list of non-zero values and the corresponding indices are in the list 'indices'
        Uses the base (parent) class attributes data (this is where 'values' are kept) and zero_test
        Length is the length of the vector - the number of entries in 'values' is just the number of non-zero entries
        You can assume that the number of entries in values and indices is the same.
        '''
        
        super(SparseVector, self).__init__(values, zero_test)
        self.data = values
        self.indices = indices
        self.length = length
        self.zero_test = zero_test
        


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        
        return self.length



    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        
        if i in self.indices:
            idx = bisect_left(self.indices,i)
            return self.data[idx]
        
        return 0
        
    
    
    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
      
     
        idx = bisect_left(self.indices,i)
        
        if i in self.indices:
            self.data[idx] = val
        
        elif(idx>self.indices[-1]):
            self.data.append(val)
            self.indices.append(i)
        
        else:
            self.data.insert(idx,val)
            self.indices.insert(idx,i)



    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        
        
        if self.data == []:
            return True
        
        return False



    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        
        
        sparse_list = [0] * self.length
        j = 0
        
        for i in self.indices:
            sparse_list[i] = self.data[j]
            j = j+1
          
        length = len(sparse_list)
        mid = length/2
        
        first_half = sparse_list[:mid]
        second_half = sparse_list[mid:]
        
        first_vector = make_vector(first_half , self.zero_test)
        second_vector = make_vector(second_half , self.zero_test)
         
        return first_vector , second_vector
        

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        
        count = len(self)
        for i in range(0 , len(vector)):
            if vector[i] != 0:
                self.data.append(vector[i])
                self.indices.append(count)
            count = count + 1
    
