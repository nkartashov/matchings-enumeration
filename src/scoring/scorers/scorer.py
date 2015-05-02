__author__ = 'nikita_kartashov'

from functools import reduce

from .cache_scorer import CacheScorer


class Scorer(object):
    def __init__(self, comment="No scorer", cache: CacheScorer=None):
        self._comment = comment
        self._cache = cache

    def __call__(self, genomes, topology, inner_nodes):
        inner_left, inner_right = inner_nodes
        return self.sum_scores(
            self.reduce_score(self.reduce_score(self.cached_score(genomes[j], inner_node) for j in topology[i])
                              for i, inner_node in enumerate(inner_nodes)), self.cached_score(inner_left, inner_right))

    def reduce_score(self, scores):
        return reduce(self.sum_scores, scores, self.null_score())

    def null_score(self):
        return 0

    def are_equal(self, left_score, right_score):
        return left_score == right_score

    def sum_scores(self, left, right):
        return left + right

    def comment(self):
        return self._comment

    def cached_score(self, left, right):
        if self._cache is None:
            return self.score(left, right)
        else:
            return self._cache.retrieve(self.__class__, left, right)

    def score(self, left, right):
        return 0

    def is_score_better(self, new_score, old_score):
        return new_score > old_score

    def is_score_worse(self, new_score, old_score):
        return new_score < old_score
