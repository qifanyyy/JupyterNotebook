#!/usr/bin/python3
import random

def sotByLastValue(tuple):
	return tuple[-1]

def sortUtxo(utxo_set, above = False):
	#sorting the UTXO set by its value
	sorted_utxo_set = sorted(utxo_set, key = sotByLastValue)
	utxo_below_total = []
	utxo_above_total = []
	output_value = amount + fee
	count = 0
	for utxo in sorted_utxo_set:
		if utxo[2] >= output_value:
			break
		elif utxo[2] < output_value:
			count += 1
	#creating two lists, one containing utxo, whose value is bellow the output amouts
	#another containing utxo that are equal to or above the output amount
	utxo_below_total = sorted_utxo_set[:count]
	utxo_above_total = sorted_utxo_set[count:]
	if above == False:
		return utxo_below_total
	else:
		return utxo_above_total

def get_inputs(utxo_set, amount, fee):
	"""
 	this function should return a subset of utxo_set
 	such that total amount in the list is
 	more than (amount + fee) and change is minimal
	"""

	"""
	Ivo's logic:
	This file is a small modification to the original you sent me.
	I wanted to find the *best* subset of inputs to create a transaction with.
	The best subset is the one that would generate the smallest change.
	This is achived by generating a population of input subsets, where each subset
	contains randomly selected utxo's.
	I assume that a large enough population, would contain an optimum or a nearly optimum
	solution on most cases.
	"""


	inputs = []
	dict = {}
	total = 0
	#Magic range;
	#Assumption: within 20 iterations a subest would definately be found
	#that satisfy the condition total >= amount + fee
	subset = sortUtxo(utxo_set, above = False)

	for num in range(1,21):
		selection = random.choice(subset)
		subset.remove(selection)
		total += selection[2]
		 # add amount to total
		inputs.append(selection)
		# append to the list
		# if we get enough amount in the inputs
		if total >= amount + fee:
			return inputs


if __name__ == '__main__':

	# available inputs for spending
	# have a form (prev_txid, prev_output, amount)
	utxo_set = [
		("7078d48ca924c92643dac992756a08bf340e096fe49680c280b37cbe3e3c6761", 0, 4786),
		("78a30be97918f2895825904585c04db79881ded24f8629c0c728e805e8577aa7", 1, 436287),
		("50366207409620e23288b2961ea7572dc620ad01721ea36a057083c9924525a4", 0, 2892),
		("1239f31407a323a40ac3c7695467d22eb1b80251cef10f28cbea704bc362a90a", 2, 854739),
		("3bd096d7d422da18b3970dbe1a701b02384a36deed3c90696408ff3b11a3d685", 1, 19382),
		("1b4abd626bdbab1eb119cd740fda10b9abb3f3b90a991a9579fcd144c16f73cc", 5, 423154),
		("e98c10c4b888fbdb9e285dac6782a373456cc88a9eb7aa73c16aa261253bae20", 1, 49382691),
	]

	amount = 470000 # amount to send
	fee = 1500 # fee
	amountAndFee = amount + fee

	data_structure = {}

	#Get inputs return a list of randomly selected inputs.
	#The function is run 199 (magic) times, each time reutrning a list of inputs
	#that is stored in a dictionary. The key of the dictionary is the total value
	#of the inputs
	#After the iternations are complete, we check the list of keys to find the
	#key with the smallest value. This key would correspond to a subset of
	#inputs that generate the least change.
	#This subset is stored in the best_selection variable and used for the transaction
	#I am aware that the keys may be overwritten if another subsets amouts to The
	#same total value, but let's ignore that for now.

	sanity_checker = 0
	for num in range(1, 200):
		inputs = get_inputs(utxo_set, amount, fee)
		total = 0
		for tuple in inputs:
			total += tuple[2]
		#check whether a combination of inputs /w same amount
		#already exists
		if total not in data_structure.keys():
			data_structure[total] = inputs
		#if yes see whether it is more efficient (less inputs)
		else:
			if len(data_structure[total]) > len(inputs):
				data_structure[total] = inputs
			else:
				#a sanity_checker to make sure that that
				#if all the options are exhausted
				#the loop does not run for no reason
				sanity_checker += 1
				if sanity_checker == 20:
					break
				else:
					continue


	print(data_structure.keys())
	print("Sanity levels reached:", sanity_checker)
	print("Number of unique subsets generated:", len(data_structure))
	print("\n")

	subset_above = sortUtxo(utxo_set, above = True)
	min_diff = min(data_structure.keys())
	if subset_above[0][2] - amountAndFee < min_diff:
		best_selection = [(subset_above[0])]
	else:
		best_selection = data_structure[min_diff]


# if utxo_above_total[0][2] - output_value < total - output_value:
#    #make sure the returned item is a list of tuples for consistency
#    return [(utxo_above_total[0])]
# else:





	# result:
	print("Requested sum: ", amount)
	print("Requested fee:", fee)
	print("UTXO subset:")
	print(best_selection)
	print("Length of the subset is:", len(best_selection))
	total = sum([txin[2] for txin in best_selection])
	print("In total:", total)
	print("Change:", total-amount-fee)
