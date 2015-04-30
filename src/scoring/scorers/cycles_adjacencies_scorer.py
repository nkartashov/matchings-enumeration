__author__ = 'nikita_kartashov'

from .scorer import Scorer
from .shared_adjacency_scorer import SharedAdjacencyScorer
from .cycles_scorer import CyclesScorer


class CyclesAdjacenciesScorer(Scorer):
    def __init__(self):
        super(CyclesAdjacenciesScorer, self).__init__("cycles & adjacencies")
        self._adjacency_scorer = SharedAdjacencyScorer()
        self._cycles_scorer = CyclesScorer()

    def null_score(self):
        return self._adjacency_scorer.null_score(), self._cycles_scorer.null_score()

    def sum_scores(self, left, right):
        return tuple(l + r for l, r in zip(left, right))

    def score(self, left, right):
        return self._adjacency_scorer.score(left, right), self._cycles_scorer.score(left, right)

    def is_score_better(self, new_score, old_score):
        return all(n > o for n, o in zip(new_score, old_score))

    def is_score_worse(self, new_score, old_score):
        return all(n < o for n, o in zip(new_score, old_score))