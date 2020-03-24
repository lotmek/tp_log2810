from collections import deque, namedtuple
import networkx as nx
import matplotlib.pyplot as plt

# cela sera utile pour assigner la valeur infini à la matrice de base
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')
Station = namedtuple('Station', 'district, hasStation')

fichierTexte = open("src/arrondissements.txt", "r")
blocks = fichierTexte.read().rsplit('\n\n')


def create_stations():
    stations = []
    for line in blocks[0].splitlines():
        line = line.split(',')
        stations.append(Station(str(line[0]), bool(line[1])))

    return {station.district: station.hasStation for station in stations}


def create_edges():
    edges = []
    for line in blocks[1].splitlines():
        line = line.split(',')
        edges.append((int(line[0]), int(line[1]), int(line[2])))

    return edges


class Graph:
    def __init__(self):
        edges = create_edges()
        self.edges = [Edge(edge[0], edge[1], edge[2]) for edge in edges] + \
                     [Edge(edge[1], edge[0], edge[2]) for edge in edges]
        self.stations = create_stations()

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

    def create_visual_graph(self):
        graph = nx.Graph()
        for edge in self.edges:
            graph.add_edge(edge.start, edge.end)
        nx.draw(graph, node_size=800, node_color="cyan", with_labels=True)
        plt.show()



graph = Graph()
graph.create_visual_graph()
print(graph.dijkstra(2, 12))
