__author__ = 'nikita_kartashov'

from itertools import combinations_with_replacement

from .shared_adjacency_scorer import SharedAdjacencyScorer
from .cycles_scorer import CyclesScorer
from .cycles_adjacencies_scorer import CyclesAdjacenciesScorer
from .cache_scorer import CacheScorer

SCORER_CLASSES = (SharedAdjacencyScorer, CyclesScorer, CyclesAdjacenciesScorer)


def build_cache(matchings):
    default_scorers = (SharedAdjacencyScorer(),
                       CyclesScorer(),)

    result_cache = CacheScorer(len(matchings), SCORER_CLASSES[:2])
    for i, j in combinations_with_replacement(range(len(matchings)), 2):
        left, right = matchings[i], matchings[j]
        for scorer in default_scorers:
            result_cache.add(scorer.__class__, i, j, scorer.score(left, right))
    return result_cache


def build_cached_scorers(matchings):
    cache = build_cache(matchings)
    return tuple(scorer(cache) for scorer in (SharedAdjacencyScorer, CyclesScorer, CyclesAdjacenciesScorer))


def resolve_multiple_result_patterns(result_patterns):
    if all(not result_pattern.is_valid() for result_pattern in result_patterns):
        return next(iter(result_patterns))
    return next(iter(reversed(list(filter(lambda rp: rp.is_valid(), result_patterns)))))