__author__ = 'nikita_kartashov'

import multiprocessing as mp
from functools import partial
from itertools import product

from scoring.scoreboard import Scoreboard
from scoring.scorers.default_scorers import DEFAULT_SCORERS, resolve_multiple_result_patterns
from topology import DEFAULT_TOPOLOGIES


def test_pattern(genomes, inner_node_configurations):
    scoreboards = [Scoreboard(genomes, scorer) for scorer in DEFAULT_SCORERS]
    for topology in DEFAULT_TOPOLOGIES:
        for inner_nodes in inner_node_configurations:
            for scoreboard in scoreboards:
                scoreboard.update(topology, inner_nodes)
    l = [scoreboard.get_result_pattern() for scoreboard in scoreboards]
    return resolve_multiple_result_patterns(l)


def enumerate_patterns(matchings):
    matchings = list(matchings)
    inner_node_configurations = list(product(matchings, repeat=2))
    genome_configurations = product(matchings, repeat=4)
    pool = mp.Pool()
    partial_test = partial(test_pattern, inner_node_configurations=inner_node_configurations)
    patterns = map(partial_test,
                        genome_configurations)
    return filter(lambda p: p.is_valid(), patterns)