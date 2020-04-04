from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt

Chemin = namedtuple('Chemin', ['Trajet', 'Cout', 'Autonomie'])


def creerGraphe(nomFichier):
    fichierTexte = open(nomFichier, "r")
    blocks = fichierTexte.read().rsplit('\n\n')
    sommets = []
    for line in blocks[0].splitlines():
        line = line.split(',')
        sommets.append(Node(int(line[0]), bool(line[1])))

    for line in blocks[1].splitlines():
        line = line.split(',')
        relierSommets(sommets[int(line[0]) - 1], sommets[int(line[1]) - 1], int(line[2]))

    return Graphe(sommets)


def relierSommets(sommet1, sommet2, distance):
    sommet1.ajouterVoisin(sommet2, distance)
    sommet2.ajouterVoisin(sommet1, distance)


def trouverCheminMinimal(listeChemins):
    chemin = listeChemins[0]
    for trajet in listeChemins:
        if trajet.Cout < chemin.Cout:
            chemin = trajet
    return chemin


class Voiture:
    def __init__(self):
        self.clients = []
        self.position = 15
        self.charge = 100
        self.cheminParcouru = None


class Node:
    def __init__(self, id, station):
        self.id = id
        self.station = bool(station)
        self.voisins = []

    def ajouterVoisin(self, node, distance):
        sommet = {'Node': node,
                  'Distance': distance}
        self.voisins.append(sommet)

    def __repr__(self):
        return str(self.id)


def plusCourtCheminDansListe(listeChemins):
    cheminCourt = listeChemins[0]
    for chemin in listeChemins:
        if chemin.Cout < cheminCourt.Cout:
            cheminCourt = chemin
    return cheminCourt


class Graphe:
    def __init__(self, sommets):
        self.sommets = sommets
        self.voiture = Voiture()

    def trouverSommet(self, id):
        return self.sommets[id - 1]

    def verification(self, chemin, *args):
        for arg in args:
            if self.trouverSommet(arg) not in chemin.Trajet:
                return False
        return True

    def cheminsDisponibles(self, debut, fin, listeChemins=None, limite=float('Inf')):
        sommetDepart = self.trouverSommet(debut)
        sommetFin = self.trouverSommet(fin)

        listeSommets = [sommetDepart]

        if listeChemins is None:
            chemin = Chemin(listeSommets, 0, 100)

        else:
            chemin = plusCourtCheminDansListe(listeChemins)

        listeCheminsConnus = [chemin]
        listeCheminsCourts = []

        while listeCheminsConnus:
            dernierNode = chemin.Trajet[-1]

            if dernierNode not in listeSommets:
                listeSommets.append(dernierNode)

            for voisin in dernierNode.voisins:
                nodeVoisin = voisin['Node']
                distance = voisin['Distance']
                if nodeVoisin not in listeSommets and chemin.Autonomie > 15 and chemin.Cout + distance < limite:
                    listeCheminsConnus.append(Chemin(chemin.Trajet + [nodeVoisin],
                                                     chemin.Cout + distance,
                                                     chemin.Autonomie - distance))

                    if nodeVoisin.station:
                        listeCheminsConnus.append(Chemin(chemin.Trajet + [nodeVoisin],
                                                         chemin.Cout + distance + 10,
                                                         100))

            listeCheminsConnus.remove(chemin)

            if listeCheminsConnus:
                chemin = trouverCheminMinimal(listeCheminsConnus)

            if chemin.Trajet[-1] == sommetFin and sommetDepart in chemin.Trajet:
                listeCheminsCourts.append(chemin)

        # for trajet in listeCheminsCourts:
        #     print(trajet)
        return listeCheminsCourts

    def detourPossible(self, debut, fin, listeChemins):
        sommetDepart = self.trouverSommet(debut)
        sommetFin = self.trouverSommet(fin)

        listeTriee = []
        for chemin in listeChemins:
            if sommetFin in chemin.Trajet and sommetDepart in chemin.Trajet \
                    and chemin.Trajet.index(sommetDepart) < chemin.Trajet.index(sommetFin):
                listeTriee.append(chemin)

        if listeTriee:
            listeChemins.clear()
            listeChemins += listeTriee
            return True
        return False

    def trierListe(self, listeChemins):
        requetes = [[16, 7], [14, 4], [10, 12], [19, 17]]
        listeTriee = []
        condition = True
        for chemin in listeChemins:
            for requete in requetes:
                sommetDepart = self.trouverSommet(requete[0])
                sommetFin = self.trouverSommet(requete[1])
                if sommetFin in chemin.Trajet and sommetDepart in chemin.Trajet \
                        and chemin.Trajet.index(sommetDepart) < chemin.Trajet.index(sommetFin):
                    condition &= True
                else:
                    condition &= False

            if condition:
                listeTriee.append(chemin)

            condition = True

        listeChemins.clear()
        listeChemins += listeTriee

    def trierChemins(self, listeChemins):
        requetes = {'Origines': [16, 14, 10, 19], 'Destinations': [7, 4, 12, 17]}
        liste = [plusCourtCheminDansListe(listeChemins)]
        for chemin in listeChemins:
            for origine in requetes['Origines']:
                sommet = self.trouverSommet(origine)
                if sommet != liste[0].Trajet[-1] and sommet in chemin.Trajet and chemin not in liste:
                    liste.append(chemin)
        listeChemins.clear()
        listeChemins += liste

    def plusCourtChemin(self, debut, fin, limite=float('Inf')):
        listeChemins = self.cheminsDisponibles(debut, fin, limite=limite)
        return plusCourtCheminDansListe(listeChemins)

    def requetes(self):
        positionDepart = 15
        requetes = [[16, 7], [14, 4]]
        listeChemins = self.cheminsDisponibles(15, 16)
        if self.detourPossible(16, 7, listeChemins):
            print(True)
        else:
            listeChemins = self.cheminsDisponibles(16, 7, listeChemins, 135)
            print(len(listeChemins))

        if self.detourPossible(14, 7, listeChemins):
            print(True)

        listeChemins = self.cheminsDisponibles(14, 4, listeChemins, 125)

        self.trierListe(listeChemins)
        print(listeChemins)

    def testLotfi(self):
        listeChemins = self.cheminsDisponibles(19, 17, limite=100)
        for chemin in listeChemins:
            if self.trouverSommet(4) in chemin.Trajet:
                print(chemin)

    def afficherGraphe(self):
        arretes = []
        texteArretes = {}
        for sommet in self.sommets:
            for voisin in sommet.voisins:
                if [voisin['Node'].id, sommet.id] not in arretes:
                    arretes.append([sommet.id, voisin['Node'].id])
                    texteArretes.update({(sommet.id, voisin['Node'].id): voisin['Distance']})

        G = nx.Graph()
        G.add_edges_from(arretes)
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
                node_size=500, node_color='pink', alpha=0.9,
                labels={node: node for node in G.nodes()})
        nx.draw_networkx_edge_labels(G, pos, edge_labels=texteArretes, font_color='red')
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    graphe = creerGraphe("src/arrondissements.txt")
    listeChemins = graphe.cheminsDisponibles(15, 16)

    print(len(listeChemins))
    graphe.trierChemins(listeChemins)
    print(len(listeChemins))
    listeChemins = graphe.cheminsDisponibles(16, 7, listeChemins, 135)
    print(len(listeChemins))
    graphe.trierChemins(listeChemins)
    print(len(listeChemins))
    listeChemins = graphe.cheminsDisponibles(7, 14, listeChemins, 135)
    print(len(listeChemins))
    graphe.trierChemins(listeChemins)
    print((listeChemins))
    listeChemins = graphe.cheminsDisponibles(14, 4, listeChemins, 135)
    print((listeChemins))
    listeChemins = graphe.cheminsDisponibles(4, 10)
    print((listeChemins))
# graphe.detourPossible(1, 19)
# graphe.afficherGraphe()
# graphe.requetes()
# graphe.testLotfi()
