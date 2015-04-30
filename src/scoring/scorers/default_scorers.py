__author__ = 'nikita_kartashov'

from .shared_adjacency_scorer import SharedAdjacencyScorer
from .cycles_scorer import CyclesScorer
from .cycles_adjacencies_scorer import CyclesAdjacenciesScorer


# Scorers are placed so the last is more valuable
DEFAULT_SCORERS = (SharedAdjacencyScorer(),
                   CyclesScorer(),
                   CyclesAdjacenciesScorer())


def resolve_multiple_result_patterns(result_patterns):
    if all(not result_pattern.is_valid() for result_pattern in result_patterns):
        return next(iter(result_patterns))
    return next(iter(reversed(list(filter(lambda rp: rp.is_valid(), result_patterns)))))