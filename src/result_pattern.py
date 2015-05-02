__author__ = 'nikita_kartashov'


class ResultPattern(object):
    def __init__(self, genomes=None, topology=None, inner_nodes=None, score=None, comment=''):
        self._genomes = genomes
        self._topology = topology
        self._inner_nodes = inner_nodes
        self._score = score
        self._comment = comment
        self._is_valid = genomes is not None and \
                         topology is not None and \
                         inner_nodes is not None and \
                         score is not None

    def restore_from_matchings(self, matchings):
        self._genomes = tuple(matchings[index] for index in self._genomes)
        self._inner_nodes = [tuple(matchings[index] for index in inner_node_configuration)
                             for inner_node_configuration in self._inner_nodes]

    def genomes(self):
        if self._is_valid:
            return self._genomes

    def topology(self):
        if self._is_valid:
            return self._topology

    def inner_nodes(self):
        if self._is_valid:
            return self._inner_nodes

    def score(self):
        if self._is_valid:
            return self._score

    def comment(self):
        if self._is_valid:
            return self._comment

    def is_valid(self):
        return self._is_valid

    def as_brief_json(self):
        fields = ["'topology': {0}".format(str(self.topology())),
                  "'inner_nodes': {0}".format(str(self.inner_nodes())),
                  "'score': {0}".format(str(self._score)),
                  "'scoring_method': {0}".format(self._comment)]
        return '{0}\n'.format('\n'.join(fields))

    def as_json(self):
        fields = ["'genomes': {0}".format(str(self.genomes())),
                  self.as_brief_json()]

        return '\n'.join(fields)

    def __str__(self):
        return self.as_json()
