__author__ = 'nikita_kartashov'

from functools import reduce


class Scorer(object):
    def __init__(self, comment="No scorer"):
        self._comment = comment

    def __call__(self, genomes, topology, inner_nodes):
        inner_left, inner_right = inner_nodes
        return self.sum_scores(
            self.reduce_score(self.reduce_score(self.score(genomes[j], inner_node) for j in topology[i])
                              for i, inner_node in enumerate(inner_nodes)), self.score(inner_left, inner_right))

    def reduce_score(self, scores):
        return reduce(self.sum_scores, scores, self.null_score())

    def null_score(self):
        return 0

    def sum_scores(self, left, right):
        return left + right

    def comment(self):
        return self._comment

    def score(self, left, right):
        return 0

    def is_score_better(self, new_score, old_score):
        return new_score > old_score

    def is_score_worse(self, new_score, old_score):
        return new_score < old_score
