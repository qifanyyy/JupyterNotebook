from colorama import Fore, Style
"""La consigne demande de nommer ce fichier ruler.py, ce que j'ai fait, mais
pour l'import je suis alors obligé d'utiliser 'from ruler import...' au lieu de
'from needleman-wunsch import...'. Peut-être que je n'utilise pas la syntaxe
correcte, mais dans le cas où 'from needleman-wunsch...' ne arche pas, essayer
'from ruler...'. Je pense que ma difficulté est liée à l'utilisation de Pyzo."""

def red_text(text):
    """Renvoie le caractère en rouge. En cas de problèmes sur l'invité de
    commande, remplacer par return text."""
    #return text
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def redify(text, char):
    new_string = ''
    for lettre in text:
        if lettre == char:
            new_string += red_text(char)
        else:
            new_string += lettre
    return new_string

class NeeWun():

    """La classe qui fait le gros du travail. Elle stocke un grand nombre
    de données, on l'utiliseras uniquement pour faire les calculs."""

    def __init__(self, s1, s2):
        self.s = (s1, s2) #Contient les deux strings comparées
        self.l = len(self.s[0]) + 1
        self.h = len(self.s[1]) + 1
        self.init_score()
        self.init_chemin()

    def init_score(self):
        """Initialise la matrice des scores, stockés en dictionnaire. On préfère le dictionnaire car il est plus rapdie qu'une matrice numpy, et que l'algorithme n'utilise pas la structure de la matrice (pas de calcul sur les colonnes par exemple)."""
        self.score = {}
        for j in range(0, self.l):
            self.score[(0, j)] = -j
        for i in range(0, self.h):
            self.score[(i, 0)] = -i

    def init_chemin(self):
        """Initialise une matrice qui pour chaque case i,j garde une trace de la case que l'on a choisi pour calculer le score de la case i,j.On a utilisé un dictionnaire. Si ce score vient de la case à gauche, on écrit True; si c'est la case au dessus, on écrit False; si c'est la case en diagonale, on écrit rien."""
        self.chemin = {}
        for j in range(0, self.l):
            self.chemin[(0, j)] = True
        for i in range(0, self.h):
            self.chemin[(i, 0)] = False

    def parcours(self):
        """Iterable qui permet de parcourir les matrice "par tranches diagonales". On parcours les cases dont la somme des indices vaut 2, puis 3, etc..."""
        for somme in range(2, self.l + 1):
            i, j = 1, somme - 1
            while i < self.h and j > 0:
                yield i, j
                i += 1
                j -= 1
        for somme in range(self.l + 1, self.l + self.h -1):
            j = self.l - 1
            i = somme - j
            while i < self.h and j > 0:
                yield i, j
                i += 1
                j -= 1

    def next(self, i, j):
        """A partir d'une case i,j vide, calcule le score de cette case a partir de ses trois voisins et garde une trace du voisin chosi pour calculer le score. C'est la fonction qui représente la plus grande partie du temps d'éxecution: elle est donc un peu optimisée, et donc moins claire. Le calcul de up, left et diag sont  modifier si l'on veut changer la pénalité de gap."""
        pi = i - 1 #Predecesseur de i. Ceci évite plusieurs opérations.
        pj = j - 1 #Predecesseur de j
        if self.s[1][pi] == self.s[0][pj]:
            diag = self.score[(pi, pj)] + 2 #Au lieu de comparer les scores éventuels, on compare leur successeur (écoonomise une addition).
        else:
            diag = self.score[(pi, pj)]
        up = self.score[(pi, j)]
        left = self.score[(i, pj)]
        if up > left: #Ces ifs multiple économisent un appel de 'max' et règle le problème en deux comparaisons.
            if up > diag:
                self.score[(i,j)] = up - 1
                self.chemin[(i,j)] = False
            else:
                self.score[(i,j)] = diag - 1
        else:
            if left > diag:
                self.score[(i,j)] = left - 1
                self.chemin[(i,j)] = True
            else:
                self.score[(i,j)] = diag - 1

    def construire_instruction(self):
        """Fonction qui effectue la phase de remontée de l'algorithme et produit des 'instructions' pour reconstruire un candidat d'alignement. Si il y a un gap, on écris un zéro, sinon un un."""
        self.instruction = [[], []]
        i, j = self.h - 1, self.l - 1
        while i != 0 or j!= 0:
            if (i,j) in self.chemin:
                if self.chemin[(i, j)]:
                    j -= 1
                    self.instruction[0].append(1)
                    self.instruction[1].append(0)
                else:
                    i -= 1
                    self.instruction[0].append(0)
                    self.instruction[1].append(1)
            else:
                i -= 1
                j -= 1
                self.instruction[0].append(1)
                self.instruction[1].append(1)

    def construire_alignement(self):
        '''Fonction qui prend une instruction et construit un candidat d'alignement'''
        ali = ['','']
        for i in range(0,2):
            p = 0
            while self.instruction[i] != []:
                if self.instruction[i].pop() == 1:
                    ali[i] += str(self.s[i][p])
                    p += 1
                else:
                    ali[i] += '='
        self.top, self.bottom = ali[0], ali[1]

    def compute(self):
        for (i, j) in self.parcours():
            self.next(i, j)
        self.construire_instruction()
        self.construire_alignement()

class Ruler():

    '''Classe que l'utilisateur utilise. Une instance ne contient que les deux antécédents et les images.'''

    def __init__(self, s1, s2):
        self.s = (s1, s2)
        self.distance = 'Inconnue: veuillez utiliser .compute()'

    def compute(self):
        '''Utilise la classe NeeWun pour faire les calculs, puis stocke un candidat d'alignement retenu. L'instance de NeeWun n'est pas conservée.'''
        tampon = NeeWun(self.s[0], self.s[1])
        tampon.compute()
        self.raw_top = tampon.top
        self.raw_bottom = tampon.bottom
        self.distance = self.calculate_dist(self.raw_top, self.raw_bottom)

    def calculate_dist(self, x, y):
        '''Calcule la distance entre deux chaines'''
        d = 0
        for (c1, c2) in zip(x, y):
            if c1 != c2:
                d += 1
            elif c1 == '=' or c2 == '=':
                d += 1
        return d

    def report(self):
        if isinstance(self.distance, str):
            raise Exception("Veuillez utiliser .compute() avant")
        else:
            self.top, self.bottom = "", ""
            red_eq = red_text('=')
            for (x, y) in zip(self.raw_top, self.raw_bottom):
                if x == '=':
                    if y != '=':
                        self.top += red_eq
                        self.bottom += y
                    else:
                        self.top += red_eq
                        self.bottom += red_eq
                elif y == '=':
                    if x != '=':
                        self.top += x
                        self.bottom += red_eq
                    else:
                        self.top += red_eq
                        self.bottom += red_eq
                else:
                    if x != y:
                        self.top += red_text(x)
                        self.bottom += red_text(y)
                    else:
                        self.top += x
                        self.bottom += y
            return self.top, self.bottom