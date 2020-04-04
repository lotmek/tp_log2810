from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt

Chemin = namedtuple('Chemin', ['Trajet', 'Cout', 'Autonomie', 'Compteur'])


def creerCompteur(listeRequetes):
    compteur = {}
    for requete in listeRequetes:
        compteur.update({requete['origine']: 0, requete['destination']: 0})
    return compteur


def creerRequetes(nomFichier):
    fichierTexte = open(nomFichier, "r")
    positionDepart = int(fichierTexte.readline())
    listeRequetes = []
    for line in fichierTexte.readlines():
        line = line.split(',')
        listeRequetes.append({'origine': int(line[1]), 'destination': int(line[2]), 'delai': int(line[3])})

    return {'positionInitiale': positionDepart, 'liste': listeRequetes}


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


def verifierTemps(fin, compteur, listeRequetes):
    for requete in listeRequetes:
        if fin == requete['destination']:
            int1 = compteur[requete['destination']]
            int2 = compteur[requete['origine']]
            difference = int1 - int2
            if difference > requete['delai']:
                return False
    return True


def clientDisponible(node, listeRequetes):
    for requete in listeRequetes:
        if node.id == requete['origine']:
            return True
    return False


class Graphe:
    def __init__(self, sommets):
        self.sommets = sommets
        self.clients = 0
        self.requetes = creerRequetes("src/requetes.txt")

    def trouverSommet(self, index):
        return self.sommets[index - 1]

    def relierCheminSommet(self, chemin, indexSommet, listeRequetes=None):
        if listeRequetes is None:
            listeRequetes = self.requetes['liste']
        sommetFin = graphe.trouverSommet(indexSommet)
        indexDernierNode = len(chemin.Trajet)
        listeSommets = []
        listeCheminsConnus = [chemin]
        dictCouts = []
        while listeCheminsConnus:
            dernierNode = chemin.Trajet[-1]

            if dernierNode not in listeSommets:
                listeSommets.append(dernierNode)

            if clientDisponible(dernierNode, listeRequetes):
                dictCouts.append({"sommet": dernierNode, "cout": chemin.Cout})

            for voisin in dernierNode.voisins:
                nodeVoisin = voisin['Node']
                distance = voisin['Distance']

                ###### VERIFIER SI ON PEUT PRENDRE UN CLIENT ##########
                # if clientDisponible(chemin, listeRequetes) and self.clients < 4:
                #     chemin.Compteur[nodeVoisin.id] = chemin.Cout

                if nodeVoisin not in listeSommets and chemin.Autonomie > 15 \
                        and verifierTemps(sommetFin.id, chemin.Compteur, listeRequetes):

                    listeCheminsConnus.append(Chemin(chemin.Trajet + [nodeVoisin],
                                                     chemin.Cout + distance,
                                                     chemin.Autonomie - distance, chemin.Compteur))

                    if nodeVoisin.station:
                        listeCheminsConnus.append(Chemin(chemin.Trajet + [nodeVoisin],
                                                         chemin.Cout + distance + 10,
                                                         100, chemin.Compteur))

            listeCheminsConnus.remove(chemin)

            if listeCheminsConnus:
                chemin = trouverCheminMinimal(listeCheminsConnus)

            if chemin.Trajet[-1] == sommetFin and chemin.Autonomie > 15:
                chemin.Compteur[sommetFin.id] = chemin.Cout
                if verifierTemps(sommetFin.id, chemin.Compteur, listeRequetes):
                    for element in dictCouts:
                        node = element["sommet"]
                        if node in chemin.Trajet[indexDernierNode:-1]:
                            chemin.Compteur[node.id] = element['cout']
                            self.clients += 1
                    return chemin

        return False

    def plusCourtChemin(self, indexDebut, indexFin, limite=float('Inf')):
        requete = [{'origine': indexDebut, 'destination': indexFin, 'delai': limite}]
        nodeDepart = self.trouverSommet(indexDebut)
        compteur = creerCompteur(requete)
        chemin = Chemin([nodeDepart], 0, 100, compteur)
        return self.relierCheminSommet(chemin, indexFin, requete)

    def traitementRequetes(self):
        requetesEnCours = self.requetes['liste'].copy()
        requetesEnCours.reverse()
        nodeDepart = self.trouverSommet(self.requetes['positionInitiale'])
        compteur = creerCompteur(requetesEnCours)
        chemin = Chemin([nodeDepart], 0, 100, compteur)
        while requetesEnCours:
            requete = requetesEnCours.pop()
            chemin_copie = chemin

            if chemin.Compteur[requete['origine']] != 0:
                chemin = self.relierCheminSommet(chemin, requete['destination'], self.requetes['liste'])
                if not chemin:
                    chemin = chemin_copie
                    chemin.Compteur[requete['origine']] = 0
                    requetesEnCours.append(requete)
                else:
                    print(chemin)
                    self.clients -= 1
            else:
                chemin = self.relierCheminSommet(chemin, requete['origine'], self.requetes['liste'])
                self.clients += 1
                if chemin:
                    chemin = self.relierCheminSommet(chemin, requete['destination'], self.requetes['liste'])
                if not chemin:
                    chemin = chemin_copie
                    print("Impossible de traiter cette requete")
                else:
                    print(chemin)
                self.clients -= 1

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
    graphe.plusCourtChemin(15, 16, 135)
    graphe.traitementRequetes()
# graphe.detourPossible(1, 19)
# graphe.afficherGraphe()
# graphe.requetes()
# graphe.testLotfi()
