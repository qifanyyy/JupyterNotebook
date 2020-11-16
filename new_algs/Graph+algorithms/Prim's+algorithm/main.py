import networkx as nx
import matplotlib.pyplot as plt
import random as random

#kao olaksica funkcija koja za primljenu granu vraca
#tezinu grane, a to je element sa indeksom 2 svake grane
def daj_tezinu_grane(grana):
    return grana[2]


class PrimovAlgoritam:

    def __init__(self):
        self.G = nx.Graph()
        self.prvo_crtanje = True
        self.color_map = []
        self.edge_map = []

        # pomocne varijable u cilju poboljsnja efikasnosti i citljivosti
        self.all_pairs = []
        self.not_added_pairs = []
        self.added_pairs = []
        self.curr_pairs = []
        self.all_nodes = []
        self.added_nodes = []
        self.not_added_nodes = []
        self.poc_cvor = None

        self.zabranjeni_indeksi = []
        self.br_dodanih = 1
        self.bestezinske_grane = []

        # uklapanje sa gui
        self.animacija_u_toku = False

        # za koristenje rucnog unosa grafa:
        self.br_cvorova = 0

        # za step by step
        self.br_iter = 0
        self.zadnja_iter = False

        # za brzinu animacije
        self.brzina_animacije = 0.1

    def setuj_animaciju(self):
        self.animacija_u_toku = True

    def resetuj_animaciju(self):
        self.animacija_u_toku = False

    #setuje brzinu animacije
    def setuj_brzinu_animacije(self, brzina):
        self.brzina_animacije = brzina

    def daj(self):
        return self.prvo_crtanje

    def dajg(self):
        return self.G

    #setuje broj cvorova
    def setuj_broj_cv(self, n):
        self.br_cvorova = n

    #metoda koja iz GUI-a kupi korisnicki unesene podatke za graf
    #te tako generise grane i cvorove grafa
    def rucni_unos_grafa(self, lista_grana):
        for i in range(0, self.br_cvorova, 1):
            self.G.add_node(i)
            self.all_nodes.append(i)
            self.not_added_nodes.append(i)

        for grana in lista_grana:
            self.G.add_edge(grana[0], grana[1], color='black', weight=grana[2])
            self.all_pairs.append((grana[0], grana[1], grana[2]))
            self.not_added_pairs.append((grana[0], grana[1], grana[2]))

    #metoda generise nasumicni dvosmjerni povezani graf pri cemu je osigurano
    #da je broj grana nasumican, kao i tezine grana te stepeni cvorova
    def generisi_nasumicni_graf_slova(self):
        for i in range(0, self.br_cvorova, 1):
            self.G.add_node(i)
            self.all_nodes.append(i)
            self.not_added_nodes.append(i)

        for i in range(int(2.5 * self.G.number_of_nodes())):
            cvor1 = random.randint(0, self.G.number_of_nodes() - 1)
            cvor2 = random.randint(0, self.G.number_of_nodes() - 1)
            while cvor1 == cvor2:
                cvor2 = random.randint(0, self.G.number_of_nodes() - 1)
            tezina = random.randint(1, 15)
            if ((cvor1, cvor2) in self.bestezinske_grane) or ((cvor2, cvor1) in self.bestezinske_grane):
                continue
            self.bestezinske_grane.append((cvor1, cvor2))
            self.G.add_edge(cvor1, cvor2, color='black', weight=tezina)
            self.all_pairs.append((cvor1, cvor2, tezina))
            self.not_added_pairs.append((cvor1, cvor2, tezina))
        print('----------------- sve grane --------')
        print('all pairs', self.all_pairs)
        print('not_added_pairs', self.not_added_pairs)
        print('----------')

    #metoda za crtanje pocetnog cvora pri cemu se ne azuriraju vrijednosti grana.
    def crtaj_cvor(self, tjt):
        if self.prvo_crtanje:
            for node in self.G:
                self.color_map.append('blue')
            for i in range(len(self.G.edges)):
                self.edge_map.append('black')
            self.prvo_crtanje = False
        else:
            for node in range(len(self.color_map)):
                if node == tjt:
                    self.color_map[node] = 'green'
            i = 0
            for e in self.G.edges:
                if e[0] == tjt or e[1] == tjt:
                    self.edge_map[i] = 'yellow'
                i += 1
        plt.pause(self.brzina_animacije)
        nx.draw_networkx(self.G, pos=nx.circular_layout(self.G),
                         node_color=self.color_map, width=3.7, with_labels=True,
                         edge_color=self.edge_map)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos=nx.circular_layout(self.G),
                                     edge_labels=labels)

    #funkcija crta grafik pri cemu azurira kako stanje po cvorovima,
    #tako i stanje po granama
    def crtaj_graf(self, tjt, grana):
        if self.prvo_crtanje:
            for node in self.G:
                self.color_map.append('blue')
            for i in range(len(self.G.edges)):
                self.edge_map.append('black')
            self.prvo_crtanje = False
        else:
            # plt.gcf().clear()
            for node in range(len(self.color_map)):
                if node == tjt:
                    self.color_map[node] = 'green'

            i = 0
            for e in self.G.edges:
                if e[0] == tjt or e[1] == tjt:
                    if not (i in self.zabranjeni_indeksi):
                        self.edge_map[i] = 'yellow'
                i += 1
            i = 0
            for e in self.G.edges:
                if (e[0] == grana[0] and e[1] == grana[1]) or (e[1] == grana[0] and e[0] == grana[1]):
                    self.edge_map[i] = 'red'
                    self.zabranjeni_indeksi.append(i)
                i += 1
        plt.pause(self.brzina_animacije)
        # pos = nx.get_node_attributes(self.G, 'pos')
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx(self.G, pos=nx.circular_layout(self.G),
                         node_color=self.color_map, width=3.7, with_labels=True,
                         edge_color=self.edge_map)
        nx.draw_networkx_edge_labels(self.G, pos=nx.circular_layout(self.G),
                                     edge_labels=labels)

    # funkcija uklanja grane koje povezuju dva cvora koja vec imamo u sastavu kostura
    def ukloni_zabranjene(self, cvor):
        pomocni = []
        for x in self.curr_pairs:
            if (x[0] == cvor and (x[1] in self.added_nodes)):
                pomocni.append(x)
            if (x[1] == cvor and (x[0] in self.added_nodes)):
                pomocni.append(x)

        for x in pomocni:
            self.curr_pairs.remove(x)

    # funkcija dodaje sve grane novododanog cvora u listu (tako da se mogu razmatrati)
    def dodaj_nove_grane(self, cvor):
        pomocni = []
        for grana in self.not_added_pairs:
            print(grana)
            if grana[0] == cvor or grana[1] == cvor:
                self.curr_pairs.append(grana)
                pomocni.append(grana)
        for grana in pomocni:
            self.not_added_pairs.remove(grana)

    # azurira cvorove, odnosno novododani cvor uklanja iz liste "nedodanih" i ubacuje u listu "dodanih"
    def azuriraj_cvorove(self, grana):
        if not (grana[0] in self.added_nodes):
            self.added_nodes.append(grana[0])
            self.not_added_nodes.remove(grana[0])
            return grana[0]

        if not (grana[1] in self.added_nodes):
            self.added_nodes.append(grana[1])
            self.not_added_nodes.remove(grana[1])
            return grana[1]

    #izvrsavanje Primovog algoritma
    def zapocni_pretragu(self):
        self.crtaj_cvor(1000)
        self.poc_cvor = 3
        self.added_nodes.append(self.poc_cvor)
        self.not_added_nodes.remove(self.poc_cvor)
        self.dodaj_nove_grane(self.poc_cvor)
        self.crtaj_cvor(self.poc_cvor)
        self.curr_pairs.sort(key=daj_tezinu_grane)
        self.br_dodanih = 1
        while True:
            print('Added nodes: ', self.added_nodes)
            print('Not added nodes: ', self.not_added_nodes)
            print('Current pairs: ', self.curr_pairs)
            print('Not_added pairs: ', self.not_added_pairs)
            print('----------------------------------------')
            self.br_dodanih += 1
            if (self.br_dodanih == len(self.all_nodes)):
                zadnji_cvor = self.not_added_nodes[0]
                self.curr_pairs.sort(key=daj_tezinu_grane)
                self.not_added_pairs.sort(key=daj_tezinu_grane)
                for x in self.curr_pairs:
                    if x[0] == zadnji_cvor or x[1] == zadnji_cvor:
                        grana = x
                grana = self.curr_pairs[0]
                x = (grana[0], grana[1])
                self.crtaj_graf(zadnji_cvor, x)
                break
            else:
                grana = self.curr_pairs[0]
                self.added_pairs.append(grana)
                self.curr_pairs.remove(grana)
                novo_dodani_cvor = self.azuriraj_cvorove(grana)
                x = (grana[0], grana[1])
                self.crtaj_graf(novo_dodani_cvor, x)
                self.dodaj_nove_grane(novo_dodani_cvor)
                self.ukloni_zabranjene(novo_dodani_cvor)
                self.curr_pairs.sort(key=daj_tezinu_grane)
        plt.pause(1)
        self.resetuj_animaciju()

    #metoda izvrsava jednu iteraciju Primovog algoritma
    #informacija o tome koja je iteracija u toku se cuva u atributu self.br_iter
    def step_by_step_iter(self):
        if self.br_iter == 0:
            self.crtaj_cvor(1000)
            self.poc_cvor = 3
            self.added_nodes.append(self.poc_cvor)
            self.not_added_nodes.remove(self.poc_cvor)
            self.dodaj_nove_grane(self.poc_cvor)
            self.crtaj_cvor(self.poc_cvor)
            self.curr_pairs.sort(key=daj_tezinu_grane)
            self.br_dodanih = 1
        else:
            print('Added nodes: ', self.added_nodes)
            print('Not added nodes: ', self.not_added_nodes)
            print('Current pairs: ', self.curr_pairs)
            print('Not_added pairs: ', self.not_added_pairs)
            print('----------------------------------------')
            self.br_dodanih += 1
            if (self.br_dodanih == len(self.all_nodes)):
                zadnji_cvor = self.not_added_nodes[0]
                self.curr_pairs.sort(key=daj_tezinu_grane)
                self.not_added_pairs.sort(key=daj_tezinu_grane)
                for x in self.curr_pairs:
                    if x[0] == zadnji_cvor or x[1] == zadnji_cvor:
                        grana = x
                grana = self.curr_pairs[0]
                x = (grana[0], grana[1])
                self.crtaj_graf(zadnji_cvor, x)
                # izmjena u odnosu na petlju
                plt.pause(3)
                self.zadnja_iter = True
            else:
                grana = self.curr_pairs[0]
                self.added_pairs.append(grana)
                self.curr_pairs.remove(grana)
                novo_dodani_cvor = self.azuriraj_cvorove(grana)
                x = (grana[0], grana[1])
                self.crtaj_graf(novo_dodani_cvor, x)
                self.dodaj_nove_grane(novo_dodani_cvor)
                self.ukloni_zabranjene(novo_dodani_cvor)
                self.curr_pairs.sort(key=daj_tezinu_grane)
        self.br_iter += 1