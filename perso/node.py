from collections import namedtuple

Chemin = namedtuple('Chemin', ['Trajet','Cout'])


class Node:
    def __init__(self, id, station):
        self.id = id
        self.station = bool(station)
        self.voisins = []

    def ajouter_voisin(self, node, distance):
        sommet = {'Node': node,
                  'Distance': distance}
        self.voisins.append(sommet)


def trouver_minimum(listeChemins):
    chemin = listeChemins[0]
    for trajet in listeChemins:
        if trajet.Cout < chemin.Cout:
            chemin = trajet
    return chemin

def printargs(*args):
    for args in args:
        if
    print(*args > 0)


if __name__ == "__main__":
    a = Node('a', True)
    b = Node('b', True)
    c = Node('c', True)
    d = Node('d', True)
    e = Node('e', True)
    f = Node('f', True)

    a.ajouter_voisin(b, 3)
    a.ajouter_voisin(c, 2)
    b.ajouter_voisin(a, 3)
    b.ajouter_voisin(d, 6)
    b.ajouter_voisin(c, 1)
    c.ajouter_voisin(b, 1)
    c.ajouter_voisin(a, 2)
    c.ajouter_voisin(e, 10)
    d.ajouter_voisin(b, 6)
    d.ajouter_voisin(f, 8)
    e.ajouter_voisin(c, 10)
    e.ajouter_voisin(f, 4)
    f.ajouter_voisin(d, 8)
    f.ajouter_voisin(e, 4)

    chemin = Chemin([a], 0)

    listeCheminsConnus = [chemin]
    listeSommets = [a]


    while chemin.Trajet[-1] != f:
        for voisin in chemin.Trajet[-1].voisins:
            if voisin['Node'] not in listeSommets:
                listeCheminsConnus.append(Chemin(chemin.Trajet + [voisin['Node']],
                                                 chemin.Cout + voisin['Distance']))

        listeCheminsConnus.remove(chemin)
        chemin = trouver_minimum(listeCheminsConnus)
        listeSommets.append(chemin.Trajet[-1])

    for sommet in chemin.Trajet:
        print(sommet.id)

    printargs(1,2,3,4)
