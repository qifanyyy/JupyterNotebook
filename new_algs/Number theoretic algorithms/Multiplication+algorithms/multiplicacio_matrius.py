import pywren_ibm_cloud as pywren
import numpy as npy
import pickle
import time
from COS_backend import COSBackend

#Modificar paràmetres del cos_config
cos_config = {'endpoint': 'el teu endpoint',
            'secret_key':'el teu secret key',
            'access_key':'el teu access key'}
cos = COSBackend(cos_config)

iterdata = []
m = 1700   #ROWS_A
n= 1700  #COLUMNS_A=ROWS_B
a = 170  #mida_chunk
l= 1700  #COLUMNS_B
NUMBER_RANG = 10
sequencial=0    #0=false , 1=true
elapsed_time = 0.0

def my_map_function(id,worker):
    cos = COSBackend(cos_config)
    i=int(worker/int(l/a))
    j=worker%int(l/a)
    chunkA = cos.get_object('bucket-sd', 'chunkA_' + str (i))
    chunkA=pickle.loads(chunkA)
    chunkB = cos.get_object('bucket-sd', 'chunkB_' + str (j))
    chunkB=pickle.loads(chunkB)

    C=npy.dot(chunkA,chunkB)
    cos.put_object('bucket-sd', 'chunkC_(' + str(i) + ',' + str(j) + ')', pickle.dumps(C))

    return C

def inicialitzar_matrius(seq):
    cos = COSBackend(cos_config)
    if (seq==0):
        for i in range(0,int(m/a)):
            A = npy.random.randint(NUMBER_RANG, size=(a,n))
            cos.put_object('bucket-sd', 'chunkA_' + str(i), pickle.dumps(A))
        for j in range(0,int(l/a)):
            B = npy.random.randint(NUMBER_RANG, size=(n,a))
            cos.put_object('bucket-sd', 'chunkB_' + str(j), pickle.dumps(B))
    else :
        A = npy.random.randint(NUMBER_RANG, size=(m,n))
        B = npy.random.randint(NUMBER_RANG, size=(n,l))
        cos.put_object('bucket-sd', 'MATRIU_A', pickle.dumps(A))
        cos.put_object('bucket-sd', 'MATRIU_B', pickle.dumps(B))
    return

def mult_sequencial(x):
    cos = COSBackend(cos_config)
    A = cos.get_object('bucket-sd', 'MATRIU_A')
    A =pickle.loads(A)
    B = cos.get_object('bucket-sd', 'MATRIU_B')
    B =pickle.loads(B)
    C=npy.dot(A,B)
    cos.put_object('bucket-sd', 'MATRIU_C', pickle.dumps(C))
    return C

if __name__ == "__main__":
    pw = pywren.ibm_cf_executor()

    if (sequencial!=0) and (sequencial!=1):
        print("Versió no disponible \n\tSeqüencial == 0 : versió paral·lela\n\tSeqüencial == 1 : versió seqüencial")
        exit()

    if (sequencial == 0):

        if (m%a != 0 or l%a!=0):
            print("Valor de a incorrecte.")
            exit()
        
        workers=int(m/a)*int(l/a)

        if workers > 100:
            print("El número de workers sobrepassa el màxim: 100")
            exit()

        for i in range(0,workers):
            iterdata.append(i)
    
        #Descomentar per veure el contingut de iterdata (seqüència de keys dels workers que va de 0 a (m/a)*(l/a))
        """
        print(iterdata)
        """

    #Ens hem d'assegurar que les matrius inicials s'han acabat de penjar, per tant ens esperem
    #abans de començar a calcular el temps perquè podria passar que la funció my_map_function o mult_sequencial
    #agafin matrius corresponents a execucions prèvies amb el mateix nom i això doni resultats erronis

    futures=pw.call_async(inicialitzar_matrius,sequencial)
    pw.wait(futures)
    pw.clean()

    start_time = time.time()
    
    #####################
    #VERSIO PARAL·LELA :#
    #####################

    if (sequencial == 0 ) : 
        #Descomentar aquesta part si es vol veure les matrius generades
        #S'ha de tenir en compte que si es descomenta que esdevindrà una 
        # execució més lenta
        """           
        for i in range(0,int(m/a)):
            chunkA = cos.get_object('bucket-sd', 'chunkA_' + str (i))
            chunkA=pickle.loads(chunkA)
            print("ChunkA_"+str(i)+":")
            print(chunkA)
        for i in range(0,int(l/a)):
            chunkB = cos.get_object('bucket-sd', 'chunkB_' + str (i))
            chunkB=pickle.loads(chunkB)
            print("ChunksB_"+str(i)+":")
            print(chunkB)
        """

        futureCalcul=pw.map(my_map_function, iterdata)   
        
        #Comprovació de resultats, descomentar si es vol mostrar per pantalla el càlcul de les matrius C
        #NOTA: descomentar aquest apartat afectarà el rendiment d'execució o increment de temps.
        #NOTA2: si es descomenta aquesta part, comentar les dos linies següents (el clean  el wait)
        """
        print(pw.get_result())
        pw.clean()
        """
        pw.clean()     
        pw.wait(futureCalcul)
    
    #####################
    #VERSIO SEQÜENCIAL :#
    #####################

    else :
        #Descomentar aquesta part si es vol veure les matrius generades
        """
        print(pickle.loads(cos.get_object('bucket-sd', 'MATRIU_A')))
        print(pickle.loads(cos.get_object('bucket-sd', 'MATRIU_B')))
        """
        
        futureCalcul=pw.call_async(mult_sequencial, 0)
        
        #Comprovació directa del resultat de la multiplicació seqüencial
        #NOTA: descomentar aquest apartat afectarà el rendiment d'execució o increment de temps.
        #NOTA2: si es descomenta aquesta part, comentar les dos linies següents (el clean  el wait)
        """
        print(pw.get_result())
        pw.clean()
        """
        pw.clean()
        pw.wait(futureCalcul)

        #Comprovació mitjançant la descàrrega de la matriu resultant de la multiplicació seqüencial
        """
        C = cos.get_object('bucket-sd', 'MATRIU_C')
        C=pickle.loads(C)
        print(C)
        """

    elapsed_time = time.time() - start_time
    print(elapsed_time)
