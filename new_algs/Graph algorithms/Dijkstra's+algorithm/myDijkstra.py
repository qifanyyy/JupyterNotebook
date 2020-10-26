###############################################################################
####
####    Projet Informatique 2014 (http://github.com/oleveque/myDijkstra)
####    École Normale Supérieure Paris-Saclay (Ex. ENS Cachan)
####    Réalisé par Olivier Lévêque
####
###############################################################################
#Prérequis :
# - Graphviz (http://www.Graphviz.org)
# - Simple Parser (http://www.cdsoft.fr/sp)


#######################################################################
##### Bibliothèques & environement de travail
import os, sys, subprocess
import sp
##os.chdir("/Users/Olivier/Desktop") #Permet de choisir un environement de travail autre que celui où est enregistré 'myDijkstra.py'


#######################################################################
##### Parser
def Parser() :
        entier = sp.R(r'\d+') / int
        flottant = sp.R(r'\d+\.\d+') / float
        nom = sp.R(r'[a-zA-Z]\w*')
        blancs = sp.R(r'\s+')
        commentaire = sp.R(r'#.*')
        
        with sp.Separator( blancs | commentaire) :
            sommets = sp.Rule()
            arcs = sp.Rule()
            titre = sp.Rule()
            sommet = sp.Rule()
            arc = sp.Rule()
            doc = sp.Rule()
            distance = sp.Rule()
            
            doc |= '<GRAPHE' & titre & '"' & '>' & sommets & arcs & '</GRAPHE>'
            titre |= 'Name="' & nom 
            sommets |= '<SOMMETS>' & sommet[:] & '</SOMMETS>'
            arcs |= '<ARCS>' & arc[:] & '</ARCS>'
            sommet |= nom & ';'
            arc |= nom & ':' & nom & ':' & distance & ';'
            distance |= entier | flottant
        return doc

dechiffreur = Parser()


#######################################################################
##### Constante globale
itineraireListe = []


#######################################################################
##### Mes Classes
class Sommet():
    def __init__(self,sommetString):
        self.nom = sommetString
        self.listeArcsSortants = []
        self.listeResultatsDijkstra = None
        self.distanceTotale = None
        self.sommetPrecedent = None

    def __str__(self): #print
        return "Nom du sommet : "+self.nom
    def __repr__(self):
        return str(self)
    def __lt__(self, autre): #Comparaison entre 2 sommets
        if (autre.distanceTotale == None) and (self.distanceTotale != None) :
            return False #évite la comparaison entre un NoneType et un int()
        elif (autre.distanceTotale != None) and (self.distanceTotale == None):
            return True #évite la comparaison entre un NoneType et un int()
        return self.distanceTotale < autre.distanceTotale


class Arc():
    def __init__(self,SommetArrivee,poidsArc):
        self.extremite = SommetArrivee
        self.longueur = poidsArc
        
    def __str__(self): #print
        return "- Sommet d'arrivé : "+self.extremite.nom+"\n-  Longueur : "+str(self.longueur)
    def __repr__(self):
        return str(self)


class Graphe():
    def __init__(self,donneesBrutes):
        self.nom = donneesBrutes[0]
        self.listeSommets = donneesBrutes[1]
        self.listeArcs = donneesBrutes[2]
        self.dicoSommets = {}

        #Rangement des Sommets
        for som in self.listeSommets:
            self.dicoSommets[som] = Sommet(som)

        #Rangement des Arcs
        for arc in self.listeArcs:
            sommetDepart = self.dicoSommets[arc[0]]
            sommetArrivee = self.dicoSommets[arc[1]]
            sommetDepart.listeArcsSortants.append(Arc(sommetArrivee, arc[2]))

        #Application de la fonction dijkstra à tous les sommets
        for som in self.listeSommets:
            self.dicoSommets[som].listeResultatsDijkstra = self.Dijkstra(self.dicoSommets[som])

        #Détermination de l'itineraire le plus long parmis les plus courts chemins calculés
        listePlusLongChemin = self.PlusLongChemin()
        self.Dijkstra(self.dicoSommets[listePlusLongChemin[0]]) #Réinitialisation des sommetsPrecedents
        itineraireComplet = self.TrajetComplexe(listePlusLongChemin[0], listePlusLongChemin[1])

        #Création d'une page HTML pour afficher les résulats
        f = open("{}.html".format(self.nom), "w")
        f.write("<html><head><title>Projet Informatique myDijkstra - ENS Paris-Saclay</title></head><body><h2>Graphe &eacute;tudi&eacute; : {}</h2><h6><i>R&eacutealis&eacute; par Olivier L&eacute;v&ecirc;que - 2014</i></h6>".format(self.nom))
        
                #Image du graphe#
        self.Graphviz(self.nom,self.listeArcs, itineraireComplet)
        f.write('<p><img width="572" vspace="0" hspace="0" height="259" border="0" src="{}.png" alt="{}" title="{}"/><br /></p><p>Le plus long des plus courts chemins entre deux sommets est repr&eacute;sent&eacute; en rouge.</p>'.format(self.nom,self.nom,self.nom))

                #Chemin#
        f.write("<h2>Plus long des plus courts chemins : entre {} et {} de distance {}</h2>".format(listePlusLongChemin[0],listePlusLongChemin[1],listePlusLongChemin[2])+"<p>Arcs contenus dans le chemin :</p>")
        f.write("<ul>")
        for chemin in itineraireComplet:
            f.write("<li>Origine : <b>{}</b>, Extremite : <b>{}</b>, Poids : <b>{}</b></li>".format(chemin[0],chemin[1],chemin[2]))
        f.write("</ul>")
        
                #Tableau#
        f.write('<h2>Distance minimale entre les sommets :</h2><table cellpadding="10" border="1"><caption align="bottom">Distances minimales entre les sommets : la plus longue est en <b>gras</b><br/><i>(les tirets repr&eacute;sentent les chemins non d&eacute;finis)</i><br /><br/></caption><tbody><tr><th></th>')
        for som in self.listeSommets:
            f.write("<th>{}</th>".format(som))
        f.write("</tr>")
        for som in self.listeSommets:
            phrase = "<tr><th>{}</th>".format(som)
            for liste in self.dicoSommets[som].listeResultatsDijkstra:
                if liste[1] == 0:
                        liste[1] = '-' #Représente par un tiret les chemins non définis
                if liste[0] == listePlusLongChemin[1] and liste[1] == listePlusLongChemin[2]:
                    phrase = phrase+"<td><b>{}</b></td>".format(liste[1])
                else:
                    phrase = phrase+"<td>{}</td>".format(liste[1])
            phrase = phrase + "</tr>"
            f.write(phrase)
        f.close()
                #Execution du fichier HTML#
##        os.startfile("{}.html".format(self.nom)) #exécuter le fichier html (ligne de commande compatible avec Windows)
##        subprocess.call(["open" if sys.platform == "darwin" else "xdg-open", "{}.html".format(self.nom)]) #exécuter le fichier html (ligne de commande compatible avec OSX)
        
    def __str__(self): #print
        return "Nom du graphe : "+self.nom
    def __repr__(self):
        return str(self)

    #Algo de dijkstra
    def Dijkstra(self, sommetDepart):
            #Initialisation#
        listeSommetsCalcules = []
        listeSommetsProvisoires = []
        for arcExplo in sommetDepart.listeArcsSortants:
            somExplo = arcExplo.extremite
            #Condition : si 2 arcs lient les memes sommets alors seul l'arc le plus court est rangé dans la listeSommetsProvisoires
            if somExplo in listeSommetsProvisoires:
                if arcExplo.longueur < somExplo.distanceTotale:
                    somExplo.distanceTotale = arcExplo.longueur
            else:
                listeSommetsProvisoires.append(arcExplo.extremite)
                somExplo.distanceTotale = arcExplo.longueur
            somExplo.sommetPrecedent = sommetDepart
            
            #Itérations# 
        while listeSommetsProvisoires:
            somProche = min(listeSommetsProvisoires)
            listeSommetsCalcules.append(somProche)
            listeSommetsProvisoires.remove(somProche)
            for arcExplo in somProche.listeArcsSortants:
                somExplo = arcExplo.extremite
                if somExplo in listeSommetsCalcules:
                    continue # -Ne rien faire-, fait l'itération suivante de la boucle
                if somExplo in listeSommetsProvisoires:
                    if somProche.distanceTotale + arcExplo.longueur < somExplo.distanceTotale:
                        somExplo.distanceTotale = somProche.distanceTotale + arcExplo.longueur
                        somExplo.sommetPrecedent = somProche
                else:
                    listeSommetsProvisoires.append(arcExplo.extremite)
                    somExplo.distanceTotale = somProche.distanceTotale + arcExplo.longueur
                    somExplo.sommetPrecedent = somProche
                    
            #Récupération des résultats#
        listeResultatsDijkstra = []
        for som in self.listeSommets:
            if self.dicoSommets[som] in listeSommetsCalcules:
                listeResultatsDijkstra.append([som, self.dicoSommets[som].distanceTotale])
            else:
                listeResultatsDijkstra.append([som, 0]) #Lorsque le sommet n'est pas calculé, il apparait tout de meme dans la liste des résultats avec une pondération nulle                 
        listeResultatsDijkstra.sort(key=lambda element:element[0]) #Trie la liste des résultats dans l'ordre alphabétique des sommets
        return listeResultatsDijkstra

    #Renvoie l'origine, l'extremite et la longueur du plus long des plus courts chemins
    def PlusLongChemin(self):
        listeChemins = []
        for som in self.listeSommets:
            listeCheminElementaire = max(self.dicoSommets[som].listeResultatsDijkstra, key=lambda element:element[1])
            listeChemins.append((som,listeCheminElementaire[0],listeCheminElementaire[1]))
        listePlusLongChemin = max(listeChemins, key=lambda element:element[2])
        return listePlusLongChemin

    #Détermine l'itinéraire exact du plus long des plus courts chemins (Technique des tours d'Hanoie)
    def TrajetSimple(self, origine, extremite):
        poids = None
        for arc in self.dicoSommets[origine].listeArcsSortants:
            if arc.extremite.nom == extremite:
                if poids == None:
                    poids = arc.longueur
                else:
                    if poids > arc.longueur:
                        poids = arc.longueur
        return (origine,extremite,poids)
    def TrajetComplexe(self, origine, extremite):
        global itineraireListe
        if origine == self.dicoSommets[extremite].sommetPrecedent.nom:
            itineraireListe.append(self.TrajetSimple(origine, extremite))
        else:
            self.TrajetComplexe(origine, self.dicoSommets[extremite].sommetPrecedent.nom)
            itineraireListe.append(self.TrajetSimple(self.dicoSommets[extremite].sommetPrecedent.nom, extremite))
        return itineraireListe

    #Graphviz - Création d'une image .png du graphe
    def Graphviz(self, nomGraphe, arcsGraphe, arcsItineraire):
        Graphviz = open("{}.dot".format(nomGraphe), 'w') #Création d'un fichier .dot qui permettra de généré une image du graphe sous 'Graphviz'
        Graphviz.write("digraph g {")
        for arc in arcsGraphe:
            if arc in arcsItineraire:
                Graphviz.write('{} -> {} [label="{}", color=red, penwidth=2.0];'.format(arc[0],arc[1],arc[2])) #Coloration de l'itinéraire du plus long des plus courts chemins
            else:
                Graphviz.write('{} -> {} [label="{}"];'.format(arc[0],arc[1],arc[2]))
        Graphviz.write("rankdir=LR }") #'rankdir=LR' permet de générer une image horizontale
        Graphviz.close()
        os.system("dot -Tpng {}.dot > {}.png".format(nomGraphe,nomGraphe)) #Création de l'image .png du graphe à partir du terminal
        return None


#######################################################################
##### Début de l'algorithme #####
boucle = 1
while boucle == 1:
        name = input("Entrer le nom du fichier qui détient les données textuelles : ('graph-examples/Graphe1.txt' ou 'graph-examples/Graphe2.txt') ")
        try:
                doc = open(name, 'r', encoding='latin-1') #L'encoding en 'latin-1' pour ne pas avoir de soucis avec les accents
                donnees=dechiffreur(doc.read())
                doc.close()
        
                #Filtrage des eventuelles erreurs du document textuelle#
                setSommetsArcs=set()
                setSommetsDeclares=set(donnees[1])
                for arc in donnees[2]:
                   setSommetsArcs.add(arc[0])
                   setSommetsArcs.add(arc[1])
                nomGraphe, listObsolete, listeDescrArcs = donnees
                donnees = (nomGraphe, sorted(setSommetsArcs), listeDescrArcs)
                print("- Sommets déclarés en trop : ",setSommetsDeclares-setSommetsArcs,"\n- Sommets non déclarés : ",setSommetsArcs-setSommetsDeclares)
    
                G1 = Graphe(donnees)
                print("____\nLe programme s'est correctement exécuté.\n>>>>>>   Les résultats sont affichés dans le fichier : {}.html    <<<<<<".format(donnees[0]))
                boucle = 0
        except IOError:
                print(">>>>>> ATTENTION, le fichier que vous tentez d'ouvrir n'existe pas...\n____")
##### Finde l'algorithme ##### 
        
