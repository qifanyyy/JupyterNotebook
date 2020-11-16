tab = [] #initialisation de la liste tab
def selection(tab):#la fonction selection prend en argument la liste tab
   for i in range(len(tab)):#boucle for qui donne la longueur du tableau
       min = i #i est le minimum
       for j in range(i+1, len(tab)):#pour i est dans l'intervalle i+ et la longeur du tableau
            if tab[min] > tab[j]:#si le minimum est superieur a l'élément j
               min = j#donc j devient le minimum

       tmp = tab[i] #tmp represente l'élément i
       tab[i] = tab[min]#i est le plus petit élément du tableau
       tab[min] = tmp#donc tmp represente le plus petit élément du tableau
   return tab #renvoyer la liste tab

def projet_selection(tab):#cette fonction prend en argument la liste tab
    tab = [] #initialisation de la liste tab
    a = input("Entrez votre temps d'ecran du Lundi (en min):")
    b = input("Entrez votre temps d'ecran du Mardi (en min):")
    c = input("Entrez votre temps d'ecran du Mercredi (en min):")
    d = input("Entrez votre temps d'ecran du Jeudi (en min):")
    e = input("Entrez votre temps d'ecran du Vendredi (en min):")
    f = input("Entrez votre temps d'ecran du Samedi (en min):")
    g = input("Entrez votre temps d'ecran du Dimanche (en min):")#Ces 7 variables (a,b,c,d,e,f,g) affichent dans la console les phrases suivantes"Entrez votre temps d'ecran du (Lundi,Mardi,Mercredi,Jeudi,Vendredi,Samedi et Dimanche)"
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    e = int(e)
    f = int(f)
    g = int(g)#Les 7 dernieres varibales sont des nombres entiers (int)
    tab.append(a)
    tab.append(b)
    tab.append(c)
    tab.append(d)
    tab.append(e)
    tab.append(f)
    tab.append(g)#On rajoute, dans la liste tab, les valeurs données aux variables a,b,c,d,e,f et g
    selection(tab) # on fait appel à la fonction selection
    print("Voici les temps d'écran triés de cette semaine:")#puis on écrit "Voici les temps d'écran triés de cette semaine:"
    for i in range(len(tab)):
        print ("%d" %tab[i] )
    """
    Puis on affiche les valeurs données par ordre croissant aprés avoir ecrit la phrase         "Voici les temps d'écran triés de cette semaine:"
    """
    s=0 #la somme
    for n in range(0,7):#pour n dans l'intervalle 0 et 7
        s=s+tab[n] #s est égal à la somme de tout les éléments de la liste tab
    print("La moyenne hebdomadaire de votre temps d'ecran est:")
    print(s/7)#donner la moyenne

    if s/7 > 120 : #si la moyenne est supérieure a 120 donc afficher "Posez votre téléphone et allez préparer votre BAC"
        print("Posez votre téléphone et allez préparer votre BAC")
    else: # sinon afficher " Continuer comme ca !"
        print("Continuez comme ca !")

def insertion(tab):#la fonction insertion prend en argument la liste tab
    for i in range(1, len(tab)):# pour i de 1 à la longueur du tableau.
        k = tab[i]#k est le plus petit élément du tableau
        j = i-1
        while j >= 0 and k < tab[j] : #tant que j est supérieur ou égal à 0 et que k est plus petit que l'élément du tableau represantant j
                tab[j + 1] = tab[j]
                j -= 1
        tab[j + 1] = k #donc j+1 devient le plus élément du tableau

def projet_selection(tab):#cette fonction prend en argument la liste tab
    tab = [] #initialisation de la liste tab
    a = input("Entrez votre temps d'ecran du Lundi (en min):")
    b = input("Entrez votre temps d'ecran du Mardi (en min):")
    c = input("Entrez votre temps d'ecran du Mercredi (en min):")
    d = input("Entrez votre temps d'ecran du Jeudi (en min):")
    e = input("Entrez votre temps d'ecran du Vendredi (en min):")
    f = input("Entrez votre temps d'ecran du Samedi (en min):")
    g = input("Entrez votre temps d'ecran du Dimanche (en min):")#Ces 7 variables (a,b,c,d,e,f,g) affichent dans la console les phrases suivantes"Entrez votre temps d'ecran du (Lundi,Mardi,Mercredi,Jeudi,Vendredi,Samedi et Dimanche)"
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    e = int(e)
    f = int(f)
    g = int(g)#Les 7 dernieres varibales sont des nombres entiers (int)
    tab.append(a)
    tab.append(b)
    tab.append(c)
    tab.append(d)
    tab.append(e)
    tab.append(f)
    tab.append(g)#On rajoute, dans la liste tab, les valeurs données aux variables a,b,c,d,e,f et g
    selection(tab) # on fait appel à la fonction selection
    print("Voici les temps d'écran triés de cette semaine:")#puis on écrit "Voici les temps d'écran triés de cette semaine:"
    for i in range(len(tab)):
        print ("%d" %tab[i] )
    s=0 #la somme
    for n in range(0,7):#pour n dans l'intervalle 0 et 7
        s=s+tab[n] #s est égal à la somme de tout les éléments de la liste tab
    print("La moyenne hebdomadaire de votre temps d'ecran est:")
    print(s/7)#donner la moyenne

    if s/7 > 120 : #si la moyenne est supérieure a 120 donc afficher "Posez votre téléphone et allez préparer votre BAC"
        print("Posez votre téléphone et allez préparer votre BAC")
    else: # sinon afficher " Continuer comme ca !"
        print("Continuez comme ca !")
    """
    Meme fonctionnement pour la fonction d'avant (projet_selection)
    """
"""
Pour resumer, ce codage consiste à trier par ordre croissant (par selection et insertion) les temps d'écran hebdomadaire et donner leur moyenne...
"""