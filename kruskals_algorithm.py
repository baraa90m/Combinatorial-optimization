from collections import namedtuple
import random

Edge = namedtuple('Edge', ['start', 'end', 'cost'])

def create_edge(start, end, cost):
    return Edge(start, end, cost)

class Graph:

    def __init__(self, edges):
        self.edges = [create_edge(*e) for e in edges]

    def vertices(self):
        return set(
            e.start for e in self.edges
        ).union(e.end for e in self.edges)

    def get_neighbour(self, v):
        neighbours = []
        for edge in self.edges:
            if v == edge.start:
                neighbours.append((edge.end, edge.cost))

        return neighbours


    def path(self, source, destination, prev_v):
        path = []
        curr_v = destination

        while prev_v[curr_v] is not None:
            path.insert(0, curr_v)
            curr_v = prev_v[curr_v]
        path.insert(0, curr_v)

        return path

    def root(self, parents, v):
        if parents[v] == v:
            return v
        return self.root(parents, parents[v])


    def union(self, parents, u, v):
        u_root = self.root(parents, u)
        v_root = self.root(parents, v)
        parents[u_root] = v_root

    def kruskal(self):
        mst = []
        self.edges = sorted(self.edges, key=lambda item:item[2])
        prev_v = {v: v for v in self.vertices()}
        amount_edges = 0

        i = 0
        while i < len(self.vertices()) - 1:
            u, v, c = self.edges[i]
            i = i + 1

            parent_u = self.root(prev_v, u)
            parent_v = self.root(prev_v, v)

            if parent_u != parent_v:
                amount_edges += 1
                mst.append([u, v, c])
                self.union(prev_v, u, v)

        return mst

    def edges_v(self, v):
        edges_v = []
        for edge in self.edges:
            if edge.start == v or edge.end == v:
                edges_v.append(edge)
        return edges_v

    def add_vertex(self, V_mst, u, v, current_v):
        if current_v == u:
            V_mst.add(v)
            current_v = v
        else:
            V_mst.add(u)
            current_v = u
        return V_mst, current_v

    def prim(self):
        V = self.vertices()
        if not V:
            return "The graph is empty."
        random_v = random.choice(list(V))
        V_mst = set([random_v])
        edges_mst = []
        current_v = random_v

        while V_mst != V:
            edges_current_v = self.edges_v(current_v)
            if not edges_current_v:
                return "This graph is not connected."

            min_edge = min(edges_current_v, key=lambda edge: edge.cost)
            edges_mst.append(min_edge)
            V_mst, current_v = self.add_vertex(V_mst, min_edge.start, min_edge.end, current_v)

        return V_mst, edges_mst



if __name__ == '__main__':
    graph = Graph([
        ("a", "b", 2), ("a", "c", 4), ("b", "c", 5),
        ("b", "d", 4), ("b", "e", 9), ("c", "e", 1),
        ("d", "e", 2), ("c", "g", 2), ("c", "h", 7),
        ("g", "h", 3), ("g", "f", 1), ("h", "j", 5),
        ("g", "j", 8), ("f", "i", 2), ("i", "j", 6),
        ("g", "i", 6)
    ])
    print(graph.vertices())
    print(graph.prim())

