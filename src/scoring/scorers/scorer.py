__author__ = 'nikita_kartashov'

from functools import reduce

from .cache_scorer import CacheScorer


class Scorer(object):
    cache_scorer = CacheScorer()

    def __init__(self, comment="No scorer", caching=False):
        self._comment = comment
        self._caching = caching

    def __call__(self, genomes, topology, inner_nodes):
        inner_left, inner_right = inner_nodes
        return self.sum_scores(
            self.reduce_score(self.reduce_score(self.cached_score(genomes[j], inner_node) for j in topology[i])
                              for i, inner_node in enumerate(inner_nodes)), self.cached_score(inner_left, inner_right))

    def cls(self):
        return Scorer

    def reduce_score(self, scores):
        return reduce(self.sum_scores, scores, self.null_score())

    def null_score(self):
        return 0

    def sum_scores(self, left, right):
        return left + right

    def comment(self):
        return self._comment

    def cached_score(self, left, right):
        if not self._caching:
            return self.score(left, right)
        else:
            cls = self.__class__
            value = Scorer.cache_scorer.retrieve(cls, left, right)
            if value is None:
                value = self.score(left, right)
                Scorer.cache_scorer.add(cls, left, right, value)
            return value

    def score(self, left, right):
        return 0

    def is_score_better(self, new_score, old_score):
        return new_score > old_score

    def is_score_worse(self, new_score, old_score):
        return new_score < old_score
