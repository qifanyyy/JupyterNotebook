# coding: utf-8

# In[1]:

class fonetica(object):
    import nltk 
	
    def chavefoneticaBR(self,palavra,retiravogal):
        
        chave = palavra.encode('ASCII','ignore').upper()
        
        # Substituir as vogais acentuadas 
                
        chave = chave.replace("Á", "A");

        chave = chave.replace("À", "A");

        chave = chave.replace("Ã", "A");

        chave = chave.replace("Ê", "E");

        chave = chave.replace("É", "E");

        chave = chave.replace("Í", "I");

        chave = chave.replace("Ó", "O");

        chave = chave.replace("Õ", "O");

        chave = chave.replace("Ú", "U");

        
        # substituir Y por I
        
        chave = chave.replace('Y','I')
        
        # Substituimos BR por B

        chave = chave.replace('BR', 'B')

        chave = chave.replace('BL', 'B')

        # Substituimos PH por F

        chave = chave.replace('PH', 'F')

        # Substituimos GR, MG, NG, RG por G

        chave = chave.replace('MG', 'G')

        chave = chave.replace('NG', 'G')

        chave = chave.replace('RG', 'G')

        # Substituimos GE, GI, RJ, MJ, NJ por J

        chave = chave.replace('GE', 'J')

        chave = chave.replace('GI', 'J')

        chave = chave.replace('RJ', 'J')

        chave = chave.replace('MJ', 'J')

        chave = chave.replace('NJ', 'J')

        chave = chave.replace('GR', 'G')

        chave = chave.replace('GL', 'G')

        # Substituimos CE, CI e CH por S

        chave = chave.replace('CE', 'S')

        chave = chave.replace('CI', 'S')

        chave = chave.replace('CH', 'S')

        # Substituimos CT por T

        chave = chave.replace('CT', 'T')

        chave = chave.replace('CS', 'S')

        # Substituimos Q, CA, CO, CU, C por K

        chave = chave.replace('Q', 'K')

        chave = chave.replace('CA', 'K')

        chave = chave.replace('CO', 'K')

        chave = chave.replace('CU', 'K')

        chave = chave.replace('CK', 'K')

        chave = chave.replace('C', 'K')

        # Substituimos LH por L

        chave = chave.replace('LH', 'L')

        chave = chave.replace('RM', 'SM')

        # Substituimos N, RM, GM, MD, SM e Terminação AO por M

        chave = chave.replace('N', 'M')

        chave = chave.replace('GM', 'M')

        chave = chave.replace('MD', 'M')

        # Substituimos NH por N

        chave = chave.replace('NH', 'N')

        # Substituimos PR por P

        chave = chave.replace('PR', 'P')

        # Substituimos Ç, X, TS, C, Z, RS por S

        chave = chave.replace('X', 'S')

        chave = chave.replace('TS', 'S')

        chave = chave.replace('C', 'S')

        chave = chave.replace('Ç', 'S')

        chave = chave.replace('Z', 'S')

        chave = chave.replace('RS', 'S')

        # Substituimos LT, TR, CT, RT, ST por T

        chave = chave.replace('TR', 'T')

        chave = chave.replace('TL', 'T')

        chave = chave.replace('LT', 'T')

        chave = chave.replace('RT', 'T')

        chave = chave.replace('ST', 'T')

        # Substituimos W por V

        chave = chave.replace('W', 'V')
        
        #  Eliminamos as terminações S, Z, R, R, M, N, AO e L;

        tam = len(chave) - 1

        if (tam > -1):
            
            if (chave[tam]=='S' or chave[tam]=='Z' or chave[tam]=='R' or chave[tam]=='M' or chave[tam]=='N' or chave[tam]=='L'):
                
                chave = chave[0:tam]
                
        tam = len(chave) - 2

        if (tam > -1):

            if (chave[tam] == 'A' and chave[tam + 1] == 'O'):
                
                chave = chave[0:tam]

        # Substituimos L por R;

        chave = chave.replace('L', 'R')
        
        # Substituir todas as vogais 
        
        if (retiravogal):
            
            chave = chave.replace('A', '')
            chave = chave.replace('E', '')
            chave = chave.replace('I', '')
            chave = chave.replace('O', '')
            chave = chave.replace('U', '')
        
        # Substituir o H
        
        chave = chave.replace('H', '')
       
        if len(chave) > 0 : 
            chave = self.retirarrepetidas(chave)
        
        return chave

    def retirarrepetidas(self,texto): 
        
        # Eliminamos todas as letras em duplicidade;
        
        frasesaida = ''
        
        frasesaida = texto[0]
        
        
        for i in range(len(texto)):
            
            if (frasesaida[len(frasesaida) - 1] != texto[i]) or (texto[i].isdigit()):
                
                frasesaida += texto[i]
                
                
        return frasesaida        
    
    # Chave Fonetica do Roberto 
    
    
    def chavefoneticaRoberto(self,texto):    
        
        from unicodedata import normalize
        from nltk import word_tokenize
        
        consoantes = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']
        vogais = ['A','E','I','O','U']            
        
        def tratarpalavras(palavra):
            
            palavra = self.retirarrepetidas(palavra).upper()
            
            x = len(palavra)
           
            palavra = tratarconsoante(palavra)
                      
            if (palavra[0] == 'H'):
                y=1
            else:
                y=0
            
            quantidade = x-y
            
            palavra = self.retirarrepetidas(palavra)
            
            tratada = tratarvogal(palavra)
            
            if len(palavra) != len(tratada): 
                
                encontro = True
            else: 
                encontro = False
                
            tratada = tratarquantidade(tratada,quantidade,encontro)
            
            return tratada
        
        def tratarconsoante(tratar):
            
            tratar = tratar.replace('PH','F')
            tratar = tratar.replace('CH','X')
            tratar = tratar.replace('SH','X')
            tratar = tratar.replace('LH','I')
            tratar = tratar.replace('NH','I')
            tratar = tratar.replace('K','C')
            tratar = tratar.replace('Q','C')
            tratar = tratar.replace('V','U')
            tratar = tratar.replace('W','U')
            tratar = tratar.replace('Y','I')
            tratar = tratar.replace('Z','S')
            
            
            
            tam = len(tratar)
            
            tratada = ''
                                    
            for i in range(tam): 
                
                if (i+1 < tam) and ((tratar[i]=='C') or (tratar[i]=='G')): 
                
                    if ((tratar[i]=='C') and (tratar[i+1] in ['E','I','Y'])):

                        tratada += 'S'

                    elif ((tratar[i]=='G') and (tratar[i+1] in ['E','I','Y'])):           

                        tratada += 'J'
                        
                    else  :
                    
                        tratada += tratar[i]    

                elif (i+1 < tam) and (i-1 >= 0 ) and ((tratar[i]=='H') or (tratar[i]=='E')):
                                        
                    if ((tratar[i]=='H') and (tratar[i-1] in consoantes)  and (tratar[i+1] in consoantes)):           
                        
                        tratada += ''
                        
                    elif ((tratar[i]=='E') and not((tratar[i-1] == 'I') or (tratar[i+1] == 'U')) ) :     
                        
                        tratada += 'I'
                    
                    else:
                                           
                        tratada += tratar[i]
                        
                elif (tratar[i]=='Q'):
                                          
                    tratada += 'C'

                else:
                    
                    tratada += tratar[i]
             
            return tratada
        
        def tratarvogal(tratar):

            tam = len(tratar)

            tratada = ''

            seq = ''
            invogal = False

            for i in range(tam): 


                if (tratar[i] in vogais):

                    if invogal:

                        seq += tratar[i]

                    else: 

                        seq = tratar[i]
                        invogal = True

                elif invogal:

                    invogal = False

                    if len(seq) > 2:

                        seq = seq[-2:] 

                    tratada = tratada + seq + tratar[i]

                    seq = ''

                else:

                    tratada += tratar[i]  
                    
            if invogal:

                if len(seq) > 2:

                    seq = seq[-2:] 

                tratada = tratada + seq 

            return tratada

        def tratarquantidade(tratar,quantidade,inencontro):
            
            #print tratar, quantidade, inencontro
            
            tratada = ''
            
            if quantidade <=4 and not inencontro:
                
                stop = False
                
                for i in range(len(tratar)):
                    
                    
                    if tratar[i] in vogais and not stop:
                        
                        stop = True                        
                    
                    else:
                        
                        tratada += tratar[i]
                        
            elif quantidade == 5 and not inencontro:
                
                if tratar[0] in consoantes and tratar[1] in consoantes:
                    
                    stop = False
                
                    for i in range(len(tratar)):


                        if tratar[-i-1] in vogais and not stop:

                            stop = True                        

                        else:

                            tratada = tratar[-i-1] + tratada
                else:
                                       
                    tratada = tratar
                            
            elif quantidade == 6 and not inencontro:
                
                if tratar[len(tratar)-1] in consoantes:
                    
                    stop = False
                
                    for i in range(len(tratar)):

                        if tratar[i] in vogais and not stop:

                            stop = True                        

                        else:

                            tratada += tratar[i]
                            
                else:
                    
                    stop = False
                
                    for i in range(len(tratar)):


                        if tratar[-i-1] in vogais and not stop:

                            stop = True                        

                        else:

                            tratada = tratar[-i-1] + tratada

            elif quantidade >= 6:
                
                stop = False
                
                for i in range(len(tratar)):
                    
                    if tratar[-i-1] in vogais and not stop:
                        
                        stop = True                        

                    else:

                        tratada = tratar[-i-1] + tratada
            else: 
                
                tratada = tratar
                            
            return tratada        

        texto = normalize('NFKD', texto).encode('ASCII','ignore').upper()
        
        word_tokens = word_tokenize(texto)
        
        stopwords = nltk.corpus.stopwords.words('portuguese')
        
        filtro = [word.lower() for word in word_tokens if word.lower() not in stopwords]
        
        chave = ""
        
        for p in filtro:
            
            chave = chave + tratarpalavras(p) + " "
        
        return chave
        
    def metaphoneBR(self,texto): 
        
        from unicodedata import normalize
        import nltk
        from nltk import word_tokenize

        vogais = ['A','E','I','O','U']  
        
        saidas_validas = ['D','T','F','J','K','V','B','M','P']

        def tratarpalavras(tratar):
            
            tratar = tratar.upper()
            
            tam = len(tratar)
            
            consoante = ''
            
            # Substitui o Y pelo seu correspondente vocálico 
            
            tratar = tratar.replace('Y','I')
            
            for l in range(tam):
                
                letra = tratar[l]
                
                if letra == 'C':
                    
                    if (l > 0) and tratar[l-1] in ('S','X'): 
                        
                        consoante = consoante 

                    elif (l < tam -1): 
                        
                        if tratar[l+1] == 'H':
                            
                            if (l < tam -2):
                                
                                if tratar[l+2] == 'R':
                                    
                                    consoante += 'K'
                                
                                else:     
                            
                                    consoante += 'X'
                            else:
                                
                                consoante =+ 'K'                               
                                
                        
                        elif  tratar[l+1] in ['E','I']:
                            
                            consoante += 'S'  
                            
                        else:
                            
                            consoante += 'K'
                    else:

                        consoante += 'K'

                elif letra == 'G':
                                        
                    if (l < tam -1) and tratar[l+1] in ['E','I']:
                        
                        consoante += 'J'  
                        
                    elif (l < tam -2) and tratar[l+1] == 'H' and tratar[l+2] in ['E','I']:
                        
                         consoante += 'J'                    
                    
                    else: 
                            
                        consoante += 'G'
                
                elif letra == 'P':
                    
                    if (l < tam -1):
                        
                        if tratar[l+1] == 'H':
                            
                            consoante += 'F'
                        
                        else:
                            
                            consoante += 'P'
                        
                    else: 
                            
                        consoante += 'P'

                elif letra == 'L':
                    
                    if (l < tam -1) and tratar[l+1] == 'H':
                            
                        consoante += '1'  
                        
                    elif (l < tam -1) and tratar[l+1] in vogais: 
                            
                        consoante += 'L'
                    
                    elif (l==0):
                        
                        consoante += 'L'
                                            
                    else: 
                        consoante = consoante

                elif letra == 'R':
                    
                    if (l == tam-1) or (l ==0):
                            
                        consoante += '2' 
                    
                    elif (l < tam -1):
                        
                        if tratar[l+1] == 'R':
                            
                            consoante += '2'
                        
                        else:
                            
                            consoante += 'R'
                        
                    else: 
                            
                        consoante += 'R'

                elif letra == 'N':
                    
                    if (l < tam -1) and tratar[l+1] == 'H':
                            
                        consoante += '3'  

                    elif (l == tam -1) :
                            
                        consoante += 'M'  
                        
                    elif (l>0) and (tratar[l-1] != 'N'): 
                            
                        consoante += 'N'
                        
                    elif (l==0): 
                            
                        consoante += 'N'    
                        
                elif letra == 'Q':
                    
                    consoante += 'K'  

                # Se não estiver no final e for cercado por vogais, tem som de Z    
                
                elif letra == 'S':
                    
                    
                    if (l < tam -1) and (l > 0) and (tratar[l+1] == 'S'):
                        
                        consoante += 'S'
                    
                    elif (l > 0) and (tratar[l-1] == 'S'):
                        
                        consoante = consoante

                    elif (l < tam-1) and (l > 0) and (tratar[l+1] in vogais) and (tratar[l-1] in vogais):
                            
                        consoante += 'Z'  
                        

                    elif (l < tam -1) and (l > 0) and (tratar[l+1] == 'H'):
                        
                        consoante += 'X'
                    
                    elif (l < tam -1) and (tratar[l+1] == 'C'):
                        
                        if (l < tam -2) and tratar[l+2] in ['E','I']:
                            
                            consoante += 'S'

                        elif (l < tam -2) and tratar[l+2] in ['A','O','U']:
                            
                            consoante += 'SK'

                        elif (l < tam -2) and tratar[l+2] == 'H':
                            
                            consoante += 'X'
                        
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
                                                    
                            if (l == 1):

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
                    
                    consoante += 'V'
                
                elif letra in vogais:
                    
                    if l == 0:
                        
                        consoante += letra
                    
                    else: 
                        
                        consoante = consoante
                
                elif letra == 'Y':
                    
                    consoante = consoante
                
                elif letra == 'H':
                    
                    if (tam>1) and (l==0):

                        if (tratar[1] in vogais):

                            consoante += tratar[1]

                        else:
                            
                            consoante = consoante

                    else:
                        
                        consoante = consoante

                elif letra in saidas_validas:
                    
                    consoante += letra
            
            tratada = consoante
 
            return tratada
        
                
        texto = texto.upper()
        
        texto = texto.replace(U'\x87','SS')
        
        texto = normalize('NFKD', texto).encode('ASCII','ignore').upper()
        
        word_tokens = word_tokenize(texto)
        
        stopwords = nltk.corpus.stopwords.words('portuguese')
        
        filtro = [word.lower() for word in word_tokens if word.lower() not in stopwords]
        
        chave = ""
        
        for p in word_tokens:
            
            chave = chave + tratarpalavras(p) + " "
        
        return chave


# In[ ]: