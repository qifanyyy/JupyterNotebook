import Functions
def ColorerGraph(sommets, adjacents, degree):
    list_sommets_traites = []
    list_resultats = {}
    listNonAdj = []
    N_existe = True
    dict = Functions.genererDict(degree)
    j = 0 # le nombre du couleur
    for key in dict :
        if sommets[key] not in list_sommets_traites :
            list_sommets_traites += [sommets[key]]
            for i in range(len(sommets)): # ajouter les sommets non adjacent a ce sommets pour les colorer
                if i != key:
                    for adj in adjacents[i] :
                        if (adj not in list_sommets_traites) and (adj not in adjacents[key]) :
                            for elt in listNonAdj :
                                h = sommets.index(elt)
                                if adj in adjacents[h]:
                                    N_existe = False
                                    break
                            if N_existe == True:
                                list_sommets_traites += [adj]
                                listNonAdj += [adj]
                            else:
                                N_existe = True
            list_resultats["couleur "+str(j)] =[sommets[key]]+ listNonAdj
            j += 1
            listNonAdj = []
    return list_resultats

    list_sommets_traites = []
