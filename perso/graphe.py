from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt

fichierTexte = open("src/arrondissements.txt", "r")
blocks = fichierTexte.read().rsplit('\n\n')
Chemin = namedtuple('Chemin', ['Trajet', 'Cout'])


def creer_sommets():
    sommets = []
    for line in blocks[0].splitlines():
        line = line.split(',')
        sommets.append(Node(int(line[0]), bool(line[1])))

    for line in blocks[1].splitlines():
        line = line.split(',')
        relier_sommets(sommets[int(line[0]) - 1], sommets[int(line[1]) - 1], int(line[2]))

    return sommets


def relier_sommets(sommet1, sommet2, distance):
    sommet1.ajouter_voisin(sommet2, distance)
    sommet2.ajouter_voisin(sommet1, distance)


def trouver_chemin_minimal(listeChemins):
    chemin = listeChemins[0]
    for trajet in listeChemins:
        if trajet.Cout < chemin.Cout:
            chemin = trajet
    return chemin


class Node:
    def __init__(self, id, station):
        self.id = id
        self.station = bool(station)
        self.voisins = []

    def ajouter_voisin(self, node, distance):
        sommet = {'Node': node,
                  'Distance': distance}
        self.voisins.append(sommet)


class Graphe:
    def __init__(self):
        self.sommets = creer_sommets()

    def trouver_sommet(self, id):
        return self.sommets[id - 1]

    def dijkstra(self, debut, fin):
        sommet_depart = self.trouver_sommet(debut)
        sommet_fin = self.trouver_sommet(fin)

        chemin = Chemin([sommet_depart], 0)

        listeCheminsConnus = [chemin]
        listeSommets = [sommet_depart]

        while chemin.Trajet[-1] != sommet_fin:
            for voisin in chemin.Trajet[-1].voisins:
                if voisin['Node'] not in listeSommets:
                    listeCheminsConnus.append(Chemin(chemin.Trajet + [voisin['Node']],
                                                     chemin.Cout + voisin['Distance']))

            listeCheminsConnus.remove(chemin)
            chemin = trouver_chemin_minimal(listeCheminsConnus)
            listeSommets.append(chemin.Trajet[-1])

        for sommet in chemin.Trajet:
            print(sommet.id)

        return chemin

    def dessiner_graphe(self):
        graph = nx.Graph()
        for sommet in self.sommets:
            for voisin in sommet.voisins:
                graph.add_edge(sommet.id, voisin['Node'].id)
        nx.draw(graph, node_size=800, node_color="cyan", with_labels=True)
        plt.show()

graphe = Graphe()
graphe.dijkstra(2, 12)
graphe.dessiner_graphe()
