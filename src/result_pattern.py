__author__ = 'nikita_kartashov'


class ResultPattern(object):
    def __init__(self, genomes=None, topology=None, inner_nodes=None, score=None):
        self._genomes = genomes
        self._topology = topology
        self._inner_nodes = inner_nodes
        self._score = score
        self._is_valid = genomes is not None and \
                         topology is not None and \
                         inner_nodes is not None and \
                         score is not None

    def genomes(self):
        if self._is_valid:
            return self._genomes

    def topology(self):
        if self._is_valid:
            return self._genomes

    def inner_nodes(self):
        if self._is_valid:
            return self._inner_nodes

    def score(self):
        if self._is_valid:
            return self._score

    def is_valid(self):
        return self._is_valid

    def __str__(self):
        return '({0})'.format(' ,'.join([str(self.genomes()), str(self.topology()), str(self.inner_nodes())]))
