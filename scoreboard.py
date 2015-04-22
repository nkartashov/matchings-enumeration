__author__ = 'nikita_kartashov'


class Scoreboard(object):
    def __init__(self, genomes):
        self._max_score = 0
        self._genomes = genomes
        self._max_topology = None
        self._is_valid = False
        self._inner_nodes = []

    def _new_inner_nodes(self, inner_nodes):
        self._inner_nodes = [inner_nodes]

    def update(self, topology, score, inner_nodes):
        if score < self._max_score:
            return
        if score == self._max_score:
            if self._is_valid and topology == self._max_topology:
                self._inner_nodes.append(inner_nodes)
            else:
                self._is_valid = False
        else:
            self._new_best(score, topology, inner_nodes)

    def _new_best(self, score, topology, inner_nodes):
        self._max_score = score
        self._max_topology = topology
        self._new_inner_nodes(inner_nodes)
        self._is_valid = True

    def get_score(self):
        if self._is_valid:
            return self._genomes, self._max_topology, self._inner_nodes
        return None


