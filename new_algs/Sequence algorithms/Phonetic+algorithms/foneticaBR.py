# -*- coding: utf-8 -*-

class foneticaBR(object):

    def chavefonetica(self,texto):    
            
            import nltk
            from nltk import word_tokenize

            consoantes = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']
            vogais = ['A','E','I','O','U']            

            def retirarrepetidas(texto): 
        
                # Eliminamos todas as letras em duplicidade;

                frasesaida = ''

                frasesaida = texto[0]


                for i in range(len(texto)):

                    if (frasesaida[len(frasesaida) - 1] != texto[i]) or (texto[i].isdigit()):

                        frasesaida += texto[i]


                return frasesaida    

            def tratarpalavras(palavra):

                
                palavra = retirarAcentos(palavra)
                palavra = retirarrepetidas(palavra).upper()

                x = len(palavra)

                palavra = tratarconsoante(palavra)
                palavra = tratarE(palavra)

                if (palavra[0] == 'H'):
                    y=1
                else:
                    y=0

                quantidade = x-y

                palavra = retirarrepetidas(palavra)

                tratada = tratarvogal(palavra)

                encontro = testarEncontro(tratada)
                
                tratada = tratarquantidade(tratada,quantidade,encontro)

                return tratada

            def tratarE(tratar): 
                
                tam = len(tratar)

                tratada = ''

                for i in range(tam): 
                    
                    if (i+1 < tam) and (i-1 >= 0 ) and (tratar[i]=='E'):

                        if (not((tratar[i-1] == 'I') or (tratar[i+1] == 'U'))) :     

                            tratada += 'I'

                        else:

                            tratada += tratar[i] 

                    else:

                        tratada += tratar[i]

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
                tratar = tratar.replace('Ç', 'S')               
                    
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

                    elif (i+1 < tam) and (i-1 >= 0 ) and (tratar[i]=='H'):

                        if ((tratar[i]=='H') and (tratar[i-1] in consoantes)  and (tratar[i+1] in consoantes)):           

                            tratada += ''

                        else:

                            tratada += tratar[i]

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

            def testarEncontro(tratar):
                
                vogais = ['A','E','I','O','U']
                tam = len(tratar)

                tratada = ''

                letraant = ''
                invogal = False
                encontro = False

                for i in range(tam): 
                
                    if (tratar[i] in vogais):
                        
                        if (not invogal):
                            
                            invogal = True
                            
                        elif invogal:
                            
                            encontro = True
                                
                    else:
                        
                        invogal = False
                
                return encontro
            
            def tratarquantidade(tratar,quantidade,inencontro):

                #print tratar, quantidade, inencontro

                tratada = ''

                if quantidade <=4 and not inencontro:

                    stop = False

                    for i in range(len(tratar)):

                        if tratar[i] in vogais and not stop:

                            stop = True
                            tratada += tratar[i]
                            
                        elif tratar[i] in vogais and stop:

                            tratada += ''                        
                            
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

                        stop = False

                        for i in range(len(tratar)):

                            if tratar[i] in vogais and not stop:

                                stop = True
                                tratada += tratar[i]

                            elif tratar[i] in vogais and stop:

                                tratada += ''                        

                            else:

                                tratada += tratar[i]

                elif quantidade == 6 and not inencontro:

                    if tratar[len(tratar)-1] in consoantes:

                        stop = False

                        for i in range(len(tratar)):

                            if tratar[i] in vogais and not stop:

                                stop = True
                                tratada += tratar[i]

                            elif tratar[i] in vogais and stop:

                                tratada += ''                        

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
                    anterior = ''
                    
                    for i in range(len(tratar)):

                        if tratar[-i-1] in vogais and not stop:

                            stop = True                       

                            tratada = tratar[-i-1] + tratada
                            
                            anterior = tratar[-i-1]
                            
                        elif tratar[-i-1] in vogais and  stop:
                            
                            if (anterior not in vogais): 
                            
                                if (i+1 < len(tratar)):
                                
                                    if (tratar[-i-2] in vogais): 
                                        
                                        tratada = tratar[-i-1] + tratada
                                        anterior = tratar[-i-1]
                                
                                    else:
                                        
                                        tratada += ''
                                        anterior = tratar[-i-1]

                                else:
                                        
                                    tratada += ''
                                    anterior = tratar[-i-1]

                            else:
                                
                                tratada = tratar[-i-1] + tratada
                            
                        else:

                            tratada = tratar[-i-1] + tratada
                            anterior = tratar[-i-1]
                            
                else: 

                    tratada = tratar

                return tratada        
            
            def retirarAcentos(frase):
                
                 # Substituir acentos e cedilha  
                
                frase = frase.replace("Á", "A");

                frase = frase.replace("À", "A");

                frase = frase.replace("Ã", "A");

                frase = frase.replace("Ê", "E");

                frase = frase.replace("É", "E");

                frase = frase.replace("Í", "I");

                frase = frase.replace("Ó", "O");

                frase = frase.replace("Õ", "O");

                frase = frase.replace("Ú", "U");
                
                return frase
            
            texto = texto.upper()
            
            word_tokens = word_tokenize(texto)

            stopwords = nltk.corpus.stopwords.words('portuguese')

            filtro = [word.lower() for word in word_tokens if word.lower() not in stopwords]

            chave = ""

            for p in filtro:

                chave = chave + tratarpalavras(p) + " "
                
            return chave.strip()