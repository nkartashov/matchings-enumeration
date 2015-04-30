__author__ = 'nikita_kartashov'

from .scorer import Scorer


class SharedAdjacencyScorer(Scorer):
    def __init__(self):
        super(SharedAdjacencyScorer, self).__init__("shared adjacency")

    def score(self, left, right):
        return len(frozenset(left) & frozenset(right))