# coding: utf-8

class metaphoneBR(object):
    
    def chaveMetaphoneBR(self,texto): 
        
        import nltk
        
        import re 
              
        from nltk import word_tokenize

        vogais = ['A','E','I','O','U']  
        
        saidas_validas = ['1','2','3','B','D','F','J','K','L','M','P','T','V']

        def retirarAcentos(palavra):

            # Substituir acentos e cedilha  

            palavra = palavra.replace("Á", "A");

            palavra = palavra.replace("À", "A");

            palavra = palavra.replace("Ã", "A");

            palavra = palavra.replace("Ê", "E");

            palavra = palavra.replace("É", "E");

            palavra = palavra.replace("Í", "I");

            palavra = palavra.replace("Ó", "O");

            palavra = palavra.replace("Õ","O")

            palavra = palavra.replace("Ú", "U");
            
            palavra = palavra.replace("Ü", "U");
            
            return palavra

        def tratarpalavras(tratar):

            tratar = tratar.upper()

            consoante = ''
            
            # Retirar Acentos
                                      
            tratar = retirarAcentos(tratar)   
            
            # Retirar Numeros 
            
            tratar = re.sub("1|2|3|4|5|6|7|8|9","",tratar)
            
            # Substituir Ç por SS
            
            tratar = tratar.replace("Ç", "SS")
                                      
            # Substitui o Y pelo seu correspondente vocálico 
                                      
            tratar = tratar.replace('Y','I')

            # Tratar LH, NH, RR, CX
            
            tratar = tratar.replace("LH", "1")
            tratar = tratar.replace("NH", "2")
            tratar = tratar.replace("RR", "3")
            tratar = tratar.replace("XC", "SS")
            
            # Tratar TH, PH, SCH

            tratar = tratar.replace("TH", "T")
            tratar = tratar.replace("PH", "P")
            
            # tratar = tratar.replace("SCH", "X")
            
            tam = len(tratar)
            
            for l in range(tam):
                 
                letra = tratar[l]

                if letra == 'C':

                    if (l > 0) and tratar[l-1] in ('S','X'): 

                        consoante = consoante 

                    elif (l < tam -1): 

                        if tratar[l+1] == 'H':

                            consoante += 'X'                      

                        elif  tratar[l+1] in ['E','I']:

                            consoante += 'S'  

                        elif  tratar[l+1] in ['A','O','U','R']:

                            consoante += 'K'  

                elif letra == 'G':

                    if (l < tam -1) and tratar[l+1] in ['E','I']:

                        consoante += 'J'  

                    else: 

                        consoante += 'G'

                elif letra == 'R':

                    if (l == tam -1) or (l ==1):

                        consoante += '2'  

                    else: 

                        consoante += 'R'

                elif letra == 'N':

                    if (l == tam -1) :

                        consoante += 'M'  

                    elif (l>0) and (tratar[l-1] != 'N'): 

                        consoante += 'N'

                    elif (l==0): 

                        consoante += 'N'    

                elif letra == 'Q':

                    consoante += 'K'  

                # Se não estiver no final e for cercado por vogais, tem som de Z    

                elif letra == 'S':

                    if (l < tam-1):
                                                
                        if (l > 0) and (tratar[l+1] in vogais) and (tratar[l-1] in vogais):

                            consoante += 'Z'  

                        elif (l > 0) and (tratar[l+1] == 'S'):

                            consoante = consoante

                        elif (l > 0) and (tratar[l+1] == 'H'):

                            consoante += 'X'

                        elif (tratar[l+1] == 'C'):
                            
                            if (l < tam -2):

                                if tratar[l+2] in ['E','I']:

                                    consoante += 'S'

                                elif tratar[l+2] in ['A','O','U']:

                                    consoante += 'SK'

                                elif tratar[l+2] == 'H':

                                    consoante += 'X'

                                else: 

                                    consoante += 'S'
                            else: 
                                
                                consoante += 'S'                                

                        else: 

                            consoante += 'S'
                    else:
                        
                        consoante += 'S'

                elif letra == 'Z':

                    if (l == tam-1):

                        consoante += 'S'  

                    else: 

                        consoante += 'Z'

                elif letra == 'X':

                    if (l == tam-1):

                        consoante += 'X'  

                    elif (l > 0) and (tratar[l-1] == 'E'):

                        if (l < tam-2) and (tratar[l+1] in vogais):

                            if ((l-1) == 0):

                                consoante += 'Z' 

                            elif (l < tam-1) and tratar[l+1] in ('E','I'):

                                consoante += 'X'

                            else:

                                consoante += 'KS'

                        elif (l < tam-1) and (tratar[l+1]in ['C','P','T']):

                            consoante += 'S'

                        else:

                            consoante += 'KS'

                    elif (l > 0) and tratar[l-1] in vogais:

                        if (l > 1) and (tratar[l-2] in ['C','K','G','L','R','X'] or tratar[l-2] in vogais):

                            consoante += 'X'

                        else:

                            consoante += 'KS'                                          

                    else: 

                        consoante += 'X'

                elif letra == 'W':
                    
                    if (l < tam-1):
                        
                        if (tratar[l+1] in vogais):
                            
                            consoante += 'V'
                        
                        else:
                            
                            consoante += 'U'

                    consoante += 'U'

                elif letra in vogais:

                    if l == 0:

                        consoante += letra
                        
                    elif (letra == 'U') and (l > 1): 
                        
                        if tratar[l-1] in vogais: 
                            
                            consoante += 'L' 
                        
                        else:
                        
                            consoante = consoante

                    else: 

                        consoante = consoante

                elif letra in ['Y','H']:

                    consoante = consoante

                elif letra in saidas_validas:

                    consoante += letra

            tratada = consoante

            return tratada

        texto = texto.upper()

        word_tokens = word_tokenize(texto)

        stopwords = nltk.corpus.stopwords.words('portuguese')

        filtro = [word.lower() for word in word_tokens if word.lower() not in stopwords]

        chave = ""

        for p in word_tokens:
            
            
            chave = chave + tratarpalavras(p) + " "

        return chave.strip()