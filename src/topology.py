__author__ = 'nikita_kartashov'


# Topology((0, 1), (2, 3))
# translates to ((A, B), (C, D));

GENOMES = 'ABCD'


class Topology(object):
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def __getitem__(self, item):
        assert (0 <= item <= 1)
        return self._left if item == 0 else self._right

    def __str__(self):
        return self.as_newick()

    def as_newick(self):
        def letter_mapper(i):
            return GENOMES[i]

        def group_as_newick(group):
            return '({0})'.format(', '.join(map(letter_mapper, group)))

        def groups_as_newick(groups):
            return '({0});'.format(', '.join(groups))

        return groups_as_newick(group_as_newick(group) for group in (self._left, self._right))


if __name__ == '__main__':
    print(Topology((0, 1), (2, 3)).as_newick())

