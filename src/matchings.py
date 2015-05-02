__author__ = 'nikita_kartashov'

from itertools import combinations, chain


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, subset_size) for subset_size in range(1, len(s) + 1))


def is_matching_correct(edges):
    edges = list(edges)
    vertices = frozenset(s for s, e in edges) | frozenset(e for s, e in edges)
    return len(vertices) == 2 * len(edges)


def enumerate_matchings(points):
    possible_edges = combinations(range(points), 2)
    return list(filter(is_matching_correct, powerset(possible_edges)))
