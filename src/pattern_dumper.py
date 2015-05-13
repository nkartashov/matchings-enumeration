__author__ = 'nikita_kartashov'

from os import path, makedirs
from collections import defaultdict

import graphviz as gv


COLORS = ['red', 'blue', 'black', 'green']


class PatternDumper(object):
    def __init__(self, result_folder):
        self._result_folder = result_folder
        self._patterns_folder = path.join(result_folder, 'patterns')
        self._patterns_txt_file = path.join(result_folder, 'all_patterns.txt')
        self.prepare_output_folder()

    def prepare_output_folder(self):
        makedirs(self._result_folder, exist_ok=True)

    def dump_separate_patterns(self, patterns, nodes):
        pattern_numbers = defaultdict(lambda: 0)
        for pattern in patterns:
            pattern_folder_based_on_score = path.join(self._patterns_folder, pattern.comment())
            pattern_filename = path.join(pattern_folder_based_on_score,
                                         str(pattern_numbers[pattern.comment()]))
            self.dump_pattern(pattern_filename, pattern, nodes)
            pattern_numbers[pattern.comment()] += 1

    def dump_all_patterns(self, found_patterns):
        with open(self._patterns_txt_file, 'w') as output_file:
            output_file.write('\n'.join(map(str, found_patterns)))

    def dump_pattern(self, pattern_directory, pattern, nodes):
        makedirs(pattern_directory, exist_ok=True)
        result_graph = gv.Graph(filename=path.join(pattern_directory, 'pattern'), format='png')
        for i in range(nodes):
            result_graph.node(str(i))
        for i, genome in enumerate(pattern.genomes()):
            genome_color = COLORS[i]
            for edge in genome:
                head, tail = edge
                result_graph.edge(str(head), str(tail), color=genome_color)
        result_graph.render()
        with open(path.join(pattern_directory, 'summary.txt'), 'w') as summary_file:
            summary_file.write(pattern.as_json())