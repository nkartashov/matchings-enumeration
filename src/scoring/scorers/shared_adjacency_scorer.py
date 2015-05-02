__author__ = 'nikita_kartashov'

from .scorer import Scorer


class SharedAdjacencyScorer(Scorer):
    def __init__(self, caching=False):
        super(SharedAdjacencyScorer, self).__init__(comment="shared adjacency", caching=caching)

    def score(self, left, right):
        return len(frozenset(left) & frozenset(right))