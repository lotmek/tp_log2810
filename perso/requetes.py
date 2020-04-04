import graphe_lotfi as Lotfi
from collections import namedtuple

Chemin = namedtuple('Chemin', ['Trajet', 'Cout', 'Autonomie', 'Compteur'])

position = 15
requetes = [{'origine': 16, 'destination': 7, 'delai': 135},
            {'origine': 14, 'destination': 4, 'delai': 125},
            {'origine': 10, 'destination': 12, 'delai': 200},
            {'origine': 19, 'destination': 17, 'delai': 100},
            {'origine': 13, 'destination': 8, 'delai': 150},
            {'origine': 19, 'destination': 7, 'delai': 85},
            {'origine': 3, 'destination': 5, 'delai': 25},
            {'origine': 16, 'destination': 7, 'delai': 235},
            {'origine': 3, 'destination': 12, 'delai': 270}]


def creerListeOrigines(listeRequetes):
    liste = []
    grapheX = Lotfi.creerGraphe("src/arrondissements.txt")
    for requete in listeRequetes:
        liste.append(requete['origine'])
    return liste


def creerTableauRequetes(listeRequetes):
    liste = []
    # a remplacer par un self
    grapheX = Lotfi.creerGraphe("src/arrondissements.txt")
    for requete in listeRequetes:
        liste.append(requete['origine'])
        liste.append(requete['destination'])
    return liste


def verifierTemps(compteur, listeRequetes):
    for requete in listeRequetes:
        int1 = compteur[requete['destination']]
        int2 = compteur[requete['origine']]
        difference = int1 - int2
        if difference > requete['delai']:
            return False
    return True


def detourPossible(chemin1, origines, listeRequetes):
    for node in chemin1.Trajet:
        if node in origines:
            return node
    return False


def relierCheminSommet(graphe, chemin, indexSommet, listeRequetes=None, limite=float('Inf')):
    if listeRequetes is None:
        listeRequetes = requetes
    sommetFin = graphe.trouverSommet(indexSommet)

    listeSommets = []
    listeCheminsConnus = [chemin]

    while listeCheminsConnus:
        dernierNode = chemin.Trajet[-1]

        if dernierNode not in listeSommets:
            listeSommets.append(dernierNode)

        for voisin in dernierNode.voisins:
            nodeVoisin = voisin['Node']
            distance = voisin['Distance']
            if nodeVoisin not in listeSommets and chemin.Autonomie > 15 \
                    and verifierTemps(chemin.Compteur, listeRequetes):
                listeCheminsConnus.append(Chemin(chemin.Trajet + [nodeVoisin],
                                                 chemin.Cout + distance,
                                                 chemin.Autonomie - distance, chemin.Compteur))

                if nodeVoisin.station:
                    listeCheminsConnus.append(Chemin(chemin.Trajet + [nodeVoisin],
                                                     chemin.Cout + distance + 10,
                                                     100, chemin.Compteur))

        listeCheminsConnus.remove(chemin)

        if listeCheminsConnus:
            chemin = Lotfi.trouverCheminMinimal(listeCheminsConnus)

        if chemin.Trajet[-1] == sommetFin and chemin.Autonomie > 15:
            chemin.Compteur[sommetFin.id] = chemin.Cout
            if verifierTemps(chemin.Compteur, listeRequetes):
                print(chemin)
                return chemin

    return False


def plusCourtChemin(graphe, indexDebut, indexFin, limite=float('Inf')):
    requete = [{'origine': indexDebut, 'destination': indexFin, 'delai': limite}]
    chemin = Chemin([graphe.trouverSommet(indexDebut)], 0, 100, {indexDebut: 0, indexFin: 0})
    return relierCheminSommet(graphe, chemin, indexFin, requete, limite)

def cheminsDisponibles(graphe, cheminDepart, listeRequetes, limite=float('Inf')):
    tableauRequetes = creerTableauRequetes(listeRequetes)
    tableauRequetes.reverse()
    listeOrigines = creerListeOrigines(listeRequetes)
    voiture = {'nombreClients': 0}
    while tableauRequetes:
        sommetFin = graphe.trouverSommet(tableauRequetes.pop())
        if sommetFin in listeOrigines:
            listeOrigines.remove(sommetFin)

        listeSommets = []
        listeCheminsConnus = [cheminDepart]
        chemin_copie = cheminDepart
        reussite = False
        while listeCheminsConnus:
            dernierNode = cheminDepart.Trajet[-1]

            if dernierNode not in listeSommets:
                listeSommets.append(dernierNode)

            for voisin in dernierNode.voisins:
                nodeVoisin = voisin['Node']
                distance = voisin['Distance']
                if nodeVoisin not in listeSommets and cheminDepart.Autonomie > 15 \
                        and verifierTemps(cheminDepart.Compteur, requetes):
                    listeCheminsConnus.append(Chemin(cheminDepart.Trajet + [nodeVoisin],
                                                     cheminDepart.Cout + distance,
                                                     cheminDepart.Autonomie - distance, cheminDepart.Compteur))

                    if nodeVoisin.station:
                        listeCheminsConnus.append(Chemin(cheminDepart.Trajet + [nodeVoisin],
                                                         cheminDepart.Cout + distance + 10,
                                                         100, cheminDepart.Compteur))

            listeCheminsConnus.remove(cheminDepart)

            if listeCheminsConnus:
                cheminDepart = Lotfi.trouverCheminMinimal(listeCheminsConnus)

            if voiture['nombreClients'] < 4:
                node = detourPossible(cheminDepart, listeOrigines, tableauRequetes)
                if detourPossible(cheminDepart, listeOrigines, tableauRequetes):
                    voiture['nombreClients'] += 1

            if cheminDepart.Trajet[-1] == sommetFin and cheminDepart.Autonomie > 15:
                cheminDepart.Compteur[sommetFin.id] = cheminDepart.Cout
                if verifierTemps(chemin.Compteur, requetes):
                    voiture['nombreClients'] += 1
                    # retirer la requete
                    reussite = True
                    print(cheminDepart)
                    break
        if not reussite:
            cheminDepart = chemin_copie
            print("Trajet impossible")


graphe1 = Lotfi.creerGraphe("src/arrondissements.txt")

compteur1 = {16: 0, 7: 0, 14: 0, 4: 0, 10: 0, 12: 0, 19: 0, 17: 0, 13: 0, 8: 0, 3: 0, 5: 0}
tableau = [16, 7, 14, 4, 10, 12, 19, 17, 13, 8, 3, 5]
chemin1 = Chemin([graphe1.trouverSommet(15)], 0, 100, compteur1)
chemin2 = plusCourtChemin(graphe1, 15, 16, 135)
# cheminsDisponibles(graphe1, chemin, requetes)
# chemin = cheminsDisponibles(graphe1, chemin, 16)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 7)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 14)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 4)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 10)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 12)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 19)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 17)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 13)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 8)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 3)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 19)
# print(chemin)
#
# chemin_copie = chemin
# chemin = cheminsDisponibles(graphe1, chemin, 5)
#
# if chemin is None:
#     print("Il est impossible de satisfaire cette requête")
# chemin = chemin_copie
# print(chemin_copie)
# chemin = cheminsDisponibles(graphe1, chemin, 16)
# print(chemin)
# chemin = cheminsDisponibles(graphe1, chemin, 7)
# print(chemin)

# while requetes:
#     requete = requetes[0]
#     if position != requete['origine']:
#         chemin1 = graphe1.plusCourtChemin(position, requete['origine'])
