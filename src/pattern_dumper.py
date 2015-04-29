__author__ = 'nikita_kartashov'

from os import path, makedirs

import graphviz as gv


def dump_separate_patterns(folder, patterns, nodes, score_comment):
    for i, pattern in enumerate(patterns):
        pattern_filename = path.join(folder, str(i))
        dump_pattern(pattern_filename, pattern, nodes, score_comment)


def dump_all_patterns(patterns_txt_file, found_patterns):
    with open(patterns_txt_file, 'w') as output_file:
        output_file.write('\n'.join(map(str, found_patterns)))


COLORS = ['red', 'blue', 'black', 'green']


def dump_pattern(directory, pattern, nodes, score_comment):
    makedirs(directory, exist_ok=True)
    result_graph = gv.Graph(filename=path.join(directory, 'pattern'), format='png')
    for i in range(nodes):
        result_graph.node(str(i))
    for i, genome in enumerate(pattern.genomes()):
        genome_color = COLORS[i]
        for edge in genome:
            head, tail = edge
            result_graph.edge(str(head), str(tail), color=genome_color)
    result_graph.render()
    with open(path.join(directory, 'summary.txt'), 'w') as summary_file:
        summary_file.write('{0}\n'.format(pattern.topology()))
        summary_file.write('{0}\n'.format(pattern.inner_nodes()))
        summary_file.write('{0} {1}\n'.format(score_comment, pattern.score()))
