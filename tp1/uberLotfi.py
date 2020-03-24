# from djikstra import Graph
from collections import namedtuple

#
# graph = Graph([
#     ("a", "b", 3), ("a", "c", 2), ("d", "b", 2), ("d", "c", 2)])
# print(graph.dijkstra("a", "d"))
fichierTexte = open("src/arrondissements.txt", "r")
blocks = fichierTexte.read().rsplit('\n\n')
Station = namedtuple('Station', 'nom, presence')


def construireStations():
    lesStations = []
    for line in blocks[0].splitlines():
        line = line.split(',')
        lesStations.append(Station(str(line[0]), bool(line[1])))

    return {station.nom: station.presence for station in lesStations}


di = construireStations()
print(di)
