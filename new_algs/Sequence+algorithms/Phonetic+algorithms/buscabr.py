# coding: utf-8

class buscaBR(object):
    
    def chaveBR(self,palavra,retiravogal):

            chave = palavra.upper()

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

            # Substituimos CE, CI, CS e CH por S

            chave = chave.replace('CE', 'S')

            chave = chave.replace('CI', 'S')

            chave = chave.replace('CH', 'S')

            chave = chave.replace('CS', 'S')

            # Substituimos CT por T

            chave = chave.replace('CT', 'T')

            # Substituimos Q, CA, CO, CU, C por K

            chave = chave.replace('Q', 'K')

            chave = chave.replace('CA', 'K')

            chave = chave.replace('CO', 'K')

            chave = chave.replace('CU', 'K')

            chave = chave.replace('CK', 'K')

            chave = chave.replace('C', 'K')

            # Substituimos LH por L

            chave = chave.replace('LH', 'L')

            # Substituimos RM por SM
            
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

            # retirar letras repetidas
            
            if len(chave) > 0 : 
                
                saida = ''

                saida = chave[0]

                for i in range(len(chave)):

                    if (saida[len(saida) - 1] != chave[i]) or (chave[i].isdigit()):

                        saida += chave[i]
                
                chave = saida

                
            return chave
