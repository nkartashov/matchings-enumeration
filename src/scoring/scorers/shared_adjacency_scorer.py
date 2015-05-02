__author__ = 'nikita_kartashov'

from .scorer import Scorer


class SharedAdjacencyScorer(Scorer):
    def __init__(self, cache=None):
        super(SharedAdjacencyScorer, self).__init__(comment="shared adjacency", cache=cache)

    def score(self, left, right):
        return len(frozenset(left) & frozenset(right))