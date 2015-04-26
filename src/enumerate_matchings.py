__author__ = 'nikita_kartashov'

from itertools import combinations, chain, product
import multiprocessing as mp
from functools import partial
from sys import argv
from os import path, makedirs
from collections import defaultdict
from queue import Queue

from scoreboard import Scoreboard
from pattern_dumper import dump_pattern, dump_patterns


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
    inner_left, inner_right = inner_nodes
    return sum(sum(scorer(genomes[j], inner_node) for j in topology[i])
               for i, inner_node in enumerate(inner_nodes)) + scorer(inner_left, inner_right)


def shared_adjacencies_scorer(left, right):
    return len(frozenset(left) & frozenset(right))


def cycles_scorer(left, right):
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
    return filter(lambda p: p.is_valid(), patterns)


OUTPUT_RESULT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '../result'))
PATTERNS_OUTPUT_DIRECTORY = path.join(OUTPUT_RESULT_DIRECTORY, 'patterns')
PATTERNS_TXT_FILE = path.join(PATTERNS_OUTPUT_DIRECTORY, 'all_patterns.txt')


def prepare_for_output():
    makedirs(PATTERNS_OUTPUT_DIRECTORY, exist_ok=True)


def main():
    if len(argv) < 3:
        print('Need number of points & scorer (adjacencies|cycles)')
        exit(1)

    points = int(argv[1])
    scorer = None
    if argv[2] == 'adjacencies':
        scorer = shared_adjacencies_scorer
    if argv[2] == 'cycles':
        scorer = cycles_scorer
    if scorer is None:
        print('Need number of points & scorer (adjacencies|cycles)')
        exit(1)
    score_comment = argv[2]
    found_patterns = list(find_patterns(points, scorer))
    prepare_for_output()
    with open(PATTERNS_TXT_FILE, 'w') as output_file:
        output_file.write('\n'.join(map(str, found_patterns)))
    dump_patterns(PATTERNS_OUTPUT_DIRECTORY, found_patterns, points, score_comment)


if __name__ == '__main__':
    # genomes = (((0, 1), (2, 3)), ((0, 1), (2, 3)), ((1, 2),), ((0, 3),))
    # matchings = list(enumerate_matchings(4))
    # inner_node_configurations = list(product(matchings, repeat=2))
    # print(test_pattern(genomes, inner_node_configurations, cycles_scorer))
    main()
    # pattern = ((((0, 3), (1, 2)), ((0, 3), (1, 2)), ((0, 2), (1, 3)), ((0, 2), (1, 3))),
    #            ((0, 1), (2, 3)),
    #            [(((0, 3), (1, 2)), ((0, 2), (1, 3)))])
    #
    # dump_pattern(path.join(OUTPUT_RESULT_DIRECTORY, '0'), pattern, 4)