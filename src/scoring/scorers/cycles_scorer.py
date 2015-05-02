__author__ = 'nikita_kartashov'

from collections import defaultdict
from queue import Queue

from .scorer import Scorer


class CyclesScorer(Scorer):
    def __init__(self, caching=False):
        super(CyclesScorer, self).__init__(comment="cycles", caching=caching)

    def score(self, left, right):
        left = frozenset(left)
        right = frozenset(right)

        cycles_count = 0

        # Edges that are the same map to each other
        # contributing 1 cycle each
        cycles_count += len(left & right)

        adjacency_matrix = defaultdict(lambda: [])
        # Filter out all edges that were counted before
        for start, end in left ^ right:
            adjacency_matrix[start].append(end)
            adjacency_matrix[end].append(start)
        visited = defaultdict(lambda: False)
        # Mark every vertex in paths as visited
        for vertex in (vertex for vertex, neighbours in adjacency_matrix.items()
                       if len(neighbours) == 1 and not visited[vertex]):
            vertex_queue = Queue()
            vertex_queue.put(vertex)
            while not vertex_queue.empty():
                current_vertex = vertex_queue.get()
                visited[current_vertex] = True
                for v in (v for v in adjacency_matrix[current_vertex] if not visited[v]):
                    vertex_queue.put(v)

        for vertex, neighbours in adjacency_matrix.items():
            if visited[vertex]:
                continue
            next_vertex = neighbours[0]
            while True:
                parent = vertex
                vertex = next_vertex
                visited[vertex] = True
                next_vertex = next(v for v in adjacency_matrix[vertex] if v != parent)
                if visited[next_vertex]:
                    break
            cycles_count += 1

        return cycles_count