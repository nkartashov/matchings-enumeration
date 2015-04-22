__author__ = 'nikita_kartashov'

from itertools import combinations, chain, product
import multiprocessing as mp
from functools import partial
from sys import argv

from scoreboard import Scoreboard


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, subset_size) for subset_size in range(1, len(s) + 1))


def is_matching_correct(edges):
    edges = list(edges)
    vertices = frozenset(s for s, e in edges) | frozenset(e for s, e in edges)
    return len(vertices) == 2 * len(edges)


def enumerate_matchings(points):
    possible_edges = combinations(range(points), 2)
    return filter(is_matching_correct, powerset(possible_edges))

# Topologies are
# A        C
# B        D
# __________
# A        B
# C        D
# __________
# A        C
# D        B
# i.e. we follow order ABCD and translate it to numbers and then divide into 2 parts

TOPOLOGIES = \
    [((0, 1), (2, 3)),
     ((0, 2), (1, 3)),
     ((0, 3), (1, 2))]


def calculate_score(genomes, topology, scorer, inner_nodes):
    left, right = inner_nodes
    score = sum(sum(scorer(genomes[j], inner_node) for j in topology[i])
                for i, inner_node in enumerate(inner_nodes)) + scorer(left, right)
    return score


def shared_adjacencies_scorer(left, right):
    return len(frozenset(left) & frozenset(right))


def test_pattern(genomes, inner_node_configurations, scorer):
    scoreboard = Scoreboard(genomes)
    for topology in TOPOLOGIES:
        for inner_nodes in inner_node_configurations:
            score = calculate_score(genomes, topology, scorer, inner_nodes)
            scoreboard.update(topology, score, inner_nodes)
    return scoreboard.get_score()


def find_patterns(points, scorer):
    matchings = list(enumerate_matchings(points))
    inner_node_configurations = list(product(matchings, repeat=2))
    genome_configurations = product(matchings, repeat=4)
    pool = mp.Pool()
    partial_test = partial(test_pattern, scorer=scorer, inner_node_configurations=inner_node_configurations)
    patterns = pool.map(partial_test,
                        genome_configurations)
    return filter(lambda e: e is not None, patterns)


def main():
    if len(argv) < 3:
        print('Need number of points & scorer (adjacencies|cycles)')
        exit(1)

    points = int(argv[1])
    scorer = shared_adjacencies_scorer if argv[2] == 'adjacencies' else None
    if scorer is None:
        print('Need number of points & scorer (adjacencies|cycles)')
        exit(1)
    found_patterns = list(find_patterns(points, scorer))
    with open('out.txt', 'w') as output_file:
        output_file.write('\n'.join(map(str, found_patterns)))


if __name__ == '__main__':
    main()