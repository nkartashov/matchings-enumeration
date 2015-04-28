__author__ = 'nikita_kartashov'

import networkx as nx
import networkx.algorithms.isomorphism as iso


def genomes_to_multigraph(genomes):
    result = nx.MultiGraph()
    for i, genome in enumerate(genomes):
        result.add_edges_from(genome, color=i)
    return result


def are_genomes_isomorphic(left, right):
    left_graph = genomes_to_multigraph(left)
    right_graph = genomes_to_multigraph(right)
    return are_genome_graphs_isomorphic(left_graph, right_graph)


def are_genome_graphs_isomorphic(left, right):
    return iso.is_isomorphic(left, right, edge_match=lambda l, r: l == r)


def deduplicate(patterns):
    result_classes = []
    for pattern in patterns:
        genomes = pattern.genomes()
        genome_graph = genomes_to_multigraph(genomes)
        is_new = True
        for class_representative, _ in result_classes:
            if are_genome_graphs_isomorphic(class_representative, genome_graph):
                is_new = False
                break
        if is_new:
            result_classes.append((genome_graph, pattern))
    return list(map(lambda c: c[1], result_classes))


if __name__ == '__main__':
    genomes1 = (((1, 2),), ((1, 2),), ((0, 2),), ((0, 2),))
    genomes2 = (((1, 2),), ((0, 1),), ((1, 2),), ((0, 1),))
    print(are_genomes_isomorphic(genomes1, genomes2))
