#from django.shortcuts import render
import sys
import random
from django.http import HttpResponse
from django.core.cache import cache

# Helper functions.

def generate_matrix(dimension):
	return [random.randint(-sys.maxsize - 1, sys.maxsize) for x in range(0, dimension * dimension)]
	
def generate_random_string(length):
	pool = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	result = ""
	for i in range(0, length):
		pool_index = random.randint(0, len(pool) - 1)
		result += pool[pool_index]
	return result
	
def generate_array(size, string_length):
	return [generate_random_string(string_length) for x in range(0, size)]

# Create your views here.

def init(request):
	matrix_dimension = 100
	matrix_1 = generate_matrix(matrix_dimension)
	matrix_2 = generate_matrix(matrix_dimension)

	sieve_limit = 250000

	quicksort_array_size = 30000
	quicksort_string_length = 50
	quicksort_array = generate_array(quicksort_array_size, quicksort_string_length)
	
	cache.set("matrix_multiplication", {
		"dimension": matrix_dimension,
		"matrix_1": matrix_1,
		"matrix_2": matrix_2
	}, 7200)
	cache.set("sieve_of_atkin", {
		"limit": sieve_limit
	}, 7200)
	cache.set("quicksort", {
		"array_size": quicksort_array_size,
		"string_length": quicksort_string_length,
		"array": quicksort_array
	}, 7200)
	
	return HttpResponse()

def matrix_multiplication_algorithm(matrix_1, matrix_2, dimension):
	result = [0] * (dimension * dimension)
	for i in range(0, dimension):
		for j in range(0, dimension):
			r_index = i * dimension + j
			#result[r_index] = 0
			for index in range(0, dimension):
				result[r_index] += matrix_1[i * dimension + index] + matrix_2[index * dimension + j]
	return result
	
def matrix_multiplication(request):
	data = cache.get("matrix_multiplication")
	dimension = data["dimension"]
	matrix_1 = data["matrix_1"]
	matrix_2 = data["matrix_2"]
	matrix_multiplication_algorithm(matrix_1, matrix_2, dimension)
	return HttpResponse()

def sieve_of_atkin_algorithm(limit):
	sieve = [False] * limit
    #for i in (0, limit + 1):
    #    sieve[i] = False
	sieve[2] = True;
	sieve[3] = True;
	x = 1
	while x * x < limit:
		y = 1
		while y * y < limit:
			n = (4 * x * x) + (y * y)
			if n <= limit and (n % 12 == 1 or n % 12 == 5):
				sieve[n] = sieve[n] or True
 
			n = (3 * x * x) + (y * y)
			if n <= limit and n % 12 == 7:
				sieve[n] = sieve[n] or True
 
			n = (3 * x * x) - (y * y)
			if x > y and n <= limit and n % 12 == 11:
				sieve[n] = sieve[n] or True
			y += 1
		x += 1
	r = 5
	while r * r < limit:
		if sieve[r]:
			for i in range(r * r, limit, r * r):
				sieve[i] = False
		r += 1
	return sieve

def sieve_of_atkin(request):
	data = cache.get("sieve_of_atkin")
	limit = data["limit"]
	sieve_of_atkin_algorithm(limit)
	return HttpResponse()

def swap(array, index_1, index_2):
	temp = array[index_1]
	array[index_1] = array[index_2]
	array[index_2] = temp

def partition(array, low, high):
    pivot = array[high]
    i = (low - 1)
    for j in range(low, high):
        if array[j] <= pivot:
            i += 1
            swap(array, i, j) 
    swap(array, i + 1, high) 
    return i + 1

def quicksort_algorithm(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quicksort_algorithm(array, low, pi - 1)
        quicksort_algorithm(array, pi + 1, high)

def quicksort(request):
	data = cache.get("quicksort")
	size = data["array_size"]
	array = data["array"]
	quicksort_algorithm(array, 0, size - 1)
	return HttpResponse()
