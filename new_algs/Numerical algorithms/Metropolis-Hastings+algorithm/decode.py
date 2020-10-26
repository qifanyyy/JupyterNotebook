import numpy as np
import csv

with open('test/jperczel/alphabet.csv', 'rb') as csvfile:
    alphabet_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    alphabet_string = ""
    for row in alphabet_reader:
        for character in row:
            alphabet_string = alphabet_string + character[0]
#size of alphabet
alphabet_size = len(alphabet_string)

M_transition_matrix = np.genfromtxt('test/jperczel/letter_transition_matrix.csv', delimiter=',')
letter_probabilities = np.genfromtxt('test/jperczel/letter_probabilities.csv', delimiter=',')
           
##########  convert string arrays to number arrays  ############

#create distionary mapping alphabet to numbers:
char_map = {}
for num in range(0,len(alphabet_string)):
    char_map[alphabet_string[num]]=num #maps members of alphabet to numbers  

#create dictionary mappin numbers to alphabet 
num_map = {}
for num in range(0,len(alphabet_string)):
    num_map[num]=alphabet_string[num] #maps members of alphabet to numbers

#function to transform characters to numbers (a,b,c,...)=(0,1,2,...,27) & transform string into array!!!!
def char_to_num(text_in):
    output_num = np.zeros(shape=(1,len(text_in)))
    i=0
    for lines in text_in:
        for char in lines:
            if char == "\n":
                print 'issue!'
                i = i + 1
                continue 
            output_num[0,i] = char_map[char]
            i = i + 1
    return output_num

#function to transform numbers to alphabet (0,1,2,...,27) = (a,b,c,...) & transform array into string!!!!
def num_to_char(nums_in):
    output_str = ''
    for num in nums_in[0,:]:
        char = num_map[num]
        output_str = output_str + char

    return output_str

alphabet_num =  char_to_num(alphabet_string) #numerical alphabet (0,1,2,...,27)

#define dictionary to map between number_plain to number_cipher
def create_cipher_dict(cipher_function_input):
    cipher_dict = {}
    decipher_dict = {}
    for char in range(0,np.size(alphabet_num[0,:])):
        cipher_dict[alphabet_num[0,char]]=cipher_function_input[0,char]  #maps members of alphabet to cipher
        decipher_dict[cipher_function_input[0,char]]=alphabet_num[0,char]#reverse maps members of cipher to alphabet
    return (cipher_dict,decipher_dict)


#function to use permutation of numbers (e.g. 0,27,13,26,5,...) to transform text and back
def permutation_mapping(permutation_array,text_num_input,cipher_or_decipher = 'cipher'):
    (cipher_dict,decipher_dict)=create_cipher_dict(permutation_array)
    if cipher_or_decipher == 'cipher': #cipher
        dict_to_use = cipher_dict
    elif cipher_or_decipher == 'decipher': #decipher
        dict_to_use = decipher_dict
    else:
        raise Exception('Wrong mapping option!')
        
    translated_string = np.zeros(shape=np.shape(text_num_input))
    for index in range(0,np.size(text_num_input[0,:])):
        
        translated_num = dict_to_use[text_num_input[0,index]]
        translated_string[0,index] = translated_num
        
    return translated_string

def generate_next_decipher_key(f_current):
    f_updated = f_current[[0],:]
    #generate two random numbers in interval range(0,27) = 0,1,2,...,27
    entries_to_interchange = np.random.choice(alphabet_size, 2, replace=False) #NB: since the sampling is uniform, picking [(a,b) OR (b,a)] has twice the chance!
    #find entries in f_current 
    first_entry = f_current[0,entries_to_interchange[0]]
    second_entry = f_current[0,entries_to_interchange[1]]
    #interchange entries:
    f_updated[0,entries_to_interchange[0]] = second_entry
    f_updated[0,entries_to_interchange[1]] = first_entry
    
    return f_updated 
    

########### calculate likelihood function of observed ciphered text (text_num_cipher) given a specific f_current 
########### that deciphers text


#function to calculate likelihood:
def log_likelihood_of_f(y_given,f_current):
    ####use current f to decipher ciphered text:
    deciphered_text = permutation_mapping(f_current,y_given,'decipher')
        
    ####calculate relevant probabilities in Markov chain:
    p_X_0 = letter_probabilities[int(deciphered_text[0,0])]     #probability of first character
    log_p_y_F = np.log(p_X_0) #initialize likelihood probability

    for index in range(np.size(deciphered_text[0,:])-1):
        M_j = int(deciphered_text[0,index]) #the row index of matrix M_{i,j}
        M_i = int(deciphered_text[0,index+1])
        if M_transition_matrix[M_i,M_j] == 0:
            return np.nan
        log_M_i_j = np.log(M_transition_matrix[M_i,M_j])
        log_p_y_F = log_p_y_F + log_M_i_j
            
    return log_p_y_F
    

#Metropolis-Hastings algorithm:

def metropolis_hastings(ciphered_text_input):

    #decide input text:
    input_size = np.size(ciphered_text_input[0,:])

    ####(0) First start normal alphabet:
    f_state = alphabet_num
    ####(1) Find an initial state with non-zero likelihood
    log_like = log_likelihood_of_f(ciphered_text_input,f_state) #calc. initial likelihood from alphabet
    while np.isnan(log_like): #check if likelihood is non-zero
        f_state = np.random.permutation(alphabet_size).reshape((1, -1)) #if still zero, generate random new state
        log_like = log_likelihood_of_f(ciphered_text_input,f_state) #calculate loglikelihood for new state

    ####(2) run the algorithm:
#     print 'Iteration stage started.'
    total_no_of_steps = 50000 #no of steps
    recording_steps = 20 #steps to record at


    #initialize tracking of log_likelihood, accuracy and acceptance rate
    log_likelihood_iterations = np.zeros(shape=(1,total_no_of_steps/recording_steps)) 
    entropy = np.zeros(shape=(1,total_no_of_steps/recording_steps)) 
    rec_index = 0

    #number of past entropies to check
    entropy_check_no = 20 #20 works well

    #Metropolis-Hastigs steps:
    for step_no in range(total_no_of_steps):
        if step_no > entropy_check_no*recording_steps:
            #use no change in entropy as stopping condition
            entropy_change = np.abs((entropy[0,rec_index-1]-np.sum(entropy[0,rec_index-entropy_check_no:rec_index-1])/float(entropy_check_no-1))) 
            if entropy_change < entropy[0,rec_index-1]*0.001: #0.001 works well
                return f_state

        #keep track of progress of likelihood, entropy and accuracy
        if np.mod(step_no,recording_steps)==0:
            log_likelihood_iterations[0,rec_index] = log_like
            entropy[0,rec_index] = -log_like/np.log(2)/input_size
            rec_index = rec_index + 1
#             print step_no, log_like, -log_like/np.log(2)/input_size

        f_state_proposed = generate_next_decipher_key(f_state)
        log_like_proposed = log_likelihood_of_f(ciphered_text_input,f_state_proposed)
        if np.isnan(log_like_proposed): #check if likelihood is zero
            continue #likelihood=acceptance_factor = 0 anyway
        log_ratios = log_like_proposed - log_like
        #calculate min(1,exp(log_ratios):
        if log_ratios < 0:
            acceptance_factor = np.exp(log_ratios)
        elif log_ratios >= 0: #equality also corresponds to acceptance = 1
            acceptance_factor = 1
        else:
            raise Exception('Something is wrong with likelihood!')

        Bernoulli_var_A = np.random.binomial(n=1, p=acceptance_factor, size=None)
        if Bernoulli_var_A == 1:
            f_state = f_state_proposed
            log_like = log_like_proposed
        else:
            continue

        if step_no > total_no_of_steps:
            return f_state


def common_word_count(deciph_text_input):
    word_to_check = [
    'the','of','and','to','in','a','is','that','for','it','as','was','with','be','by','on',
    'not','he','i','this','are','or','his','from','at','which','but','have','an','had','they',
    'you','were','their','one','all','we','can','her','has','there','been','if','more','when',
    'will','would','who','so','no']

    input_length = np.size(deciph_text_input[[0],:])
    total_count = 0
    for word in word_to_check:
        count_plain = num_to_char(deciph_text_input).count(" "+word+" ")
        count_with_dot = num_to_char(deciph_text_input).count(" "+word+".")
        total_count = total_count + count_plain + count_with_dot
    return total_count/float(input_length)



def decode(ciphertext,out_put_filename):
    full_ciphertext_num = char_to_num(ciphertext) #whole input in numerical form
    input_text_length = np.size(full_ciphertext_num[[0],:]) #length of input
    length_to_use = min(input_text_length,10000) #use min of (input length,10000)
    
    #start work with potentially truncated input text
    ciphered_text_input = full_ciphertext_num[[0],:length_to_use]
    best_decipher = alphabet_num #just to start, will be overwritten
    best_score = 0
    for run in [1,2,3,4,5]:
        f_state = metropolis_hastings(ciphered_text_input)
        deciph_text = permutation_mapping(f_state,ciphered_text_input,'decipher')
        score = common_word_count(deciph_text)
        print score
        print f_state
        if score > best_score:
            best_decipher = f_state #overwrite with new decipher
            best_score = score #overwrite with new best score
            #make sure there is output if time-out:
            full_deciphered_text = num_to_char(permutation_mapping(best_decipher,full_ciphertext_num,'decipher'))
            #write solution to file
            f = open(out_put_filename,'w')
            f.write(full_deciphered_text)
            f.close()
    #write final solution
    full_deciphered_text = num_to_char(permutation_mapping(best_decipher,full_ciphertext_num,'decipher'))
	#write solution to file
    f = open(out_put_filename,'w')
    f.write(full_deciphered_text)
    f.close()  
