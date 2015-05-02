__author__ = 'nikita_kartashov'

from .scorer import Scorer
from .shared_adjacency_scorer import SharedAdjacencyScorer
from .cycles_scorer import CyclesScorer


class CyclesAdjacenciesScorer(Scorer):
    def __init__(self, cache=None):
        super(CyclesAdjacenciesScorer, self).__init__(comment="cycles_and_adjacencies")
        self._adjacency_scorer = SharedAdjacencyScorer(cache=cache)
        self._cycles_scorer = CyclesScorer(cache=cache)
        self._null_score_value = self._adjacency_scorer.null_score(), self._cycles_scorer.null_score()

    def null_score(self):
        return self._null_score_value

    def sum_scores(self, left, right):
        return tuple(l + r for l, r in zip(left, right))

    def cached_score(self, left, right):
        return self._adjacency_scorer.cached_score(left, right), self._cycles_scorer.cached_score(left, right)

    def is_score_better(self, new_score, old_score):
        return all(n > o for n, o in zip(new_score, old_score))

    def is_score_worse(self, new_score, old_score):
        return any(n < o for n, o in zip(new_score, old_score))

    def are_equal(self, new_score, old_score):
        return any(n == o for n, o in zip(new_score, old_score))