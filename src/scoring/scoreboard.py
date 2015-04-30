__author__ = 'nikita_kartashov'

from src.result_pattern import ResultPattern


def is_score_greater(new_score, old_score):
    return new_score > old_score


class Scoreboard(object):
    def __init__(self, genomes, scorer):
        self._genomes = genomes
        self._topology = None
        self._is_valid = False
        self._inner_nodes = []
        self._scorer = scorer
        self._score = self._scorer.null_score()

    def _new_inner_nodes(self, inner_nodes):
        self._inner_nodes = [inner_nodes]

    def update(self, topology, inner_nodes):
        score = self._scorer(self._genomes, topology, inner_nodes)
        if self._scorer.is_score_worse(score, self._score):
            return
        if score == self._score:
            if self._is_valid and topology == self._topology:
                self._inner_nodes.append(inner_nodes)
            else:
                self._is_valid = False
        else:
            self._new_best(score, topology, inner_nodes)

    def _new_best(self, score, topology, inner_nodes):
        self._score = score
        self._topology = topology
        self._new_inner_nodes(inner_nodes)
        self._is_valid = True

    def get_result_pattern(self):
        if self._is_valid:
            return ResultPattern(self._genomes, self._topology, self._inner_nodes, self._score, self._scorer.comment())
        return ResultPattern()


