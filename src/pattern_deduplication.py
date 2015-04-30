__author__ = 'nikita_kartashov'

from itertools import permutations, repeat, chain
from operator import itemgetter

import networkx as nx
import networkx.algorithms.isomorphism as iso


def genomes_to_multigraph(genomes, colors=None):
    result = nx.MultiGraph()
    if colors is None:
        colors = range(len(genomes))

    def flatten(colored_edge):
        c, (s, e) = colored_edge
        return c, s, e

    def indexed_edges(index, edges):
        return tuple(map(flatten, zip(repeat(index), edges)))

    # Take all edges and color them, then chain together
    all_edges = list(chain(*(indexed_edges(*genome) for genome in zip(colors, genomes))))

    # Sort by color, then start, then end
    for item in range(3):
        all_edges = sorted(all_edges, key=itemgetter(item))

    for i, s, e in all_edges:
        result.add_edge(s, e, color=i)

    return result


def are_genomes_isomorphic(left, right):
    left_graph = genomes_to_multigraph(left)
    right_graph = genomes_to_multigraph(right)
    return are_genome_graphs_isomorphic(left_graph, right_graph)


def are_genome_graphs_isomorphic(left, right):
    return iso.is_isomorphic(left, right, edge_match=lambda l, r: l == r)


COLOR_COMBINATIONS = None, None


def deduplicate_patterns(patterns):
    global COLOR_COMBINATIONS
    result_classes = []
    for pattern in patterns:
        genomes = pattern.genomes()
        is_new = True
        genomes_count, color_combinations = COLOR_COMBINATIONS
        if genomes_count != len(genomes):
            genomes_count = len(genomes)
            color_combinations = list(permutations(range(len(genomes))))
            COLOR_COMBINATIONS = genomes_count, color_combinations
        for colors in color_combinations:
            genome_graph = genomes_to_multigraph(genomes, colors)
            for class_representative, _ in result_classes:
                if are_genome_graphs_isomorphic(class_representative, genome_graph):
                    is_new = False
                    break
        if is_new:
            result_classes.append((genome_graph, pattern))
    return list(map(itemgetter(1), result_classes))


if __name__ == '__main__':
    pass
    # genomes1 = (((0, 1),), ((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 2),))
    # genomes2 = (((0, 1), (2, 3)), ((0, 1),), ((0, 2), (1, 3)), ((0, 2),))
    # g1 = genomes_to_multigraph(genomes1)
    # g2 = genomes_to_multigraph(genomes2, [1, 0, 2, 3])
    # print(are_genome_graphs_isomorphic(g1, g2))

