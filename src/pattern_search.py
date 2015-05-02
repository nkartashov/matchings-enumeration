__author__ = 'nikita_kartashov'

import sys
import logging as log
from os import path

from .matchings import enumerate_matchings
from .pattern_enumeration import enumerate_patterns
from .pattern_deduplication import deduplicate_patterns
from .pattern_dumper import PatternDumper


OUTPUT_RESULT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '../result'))
PATTERNS_OUTPUT_DIRECTORY = path.join(OUTPUT_RESULT_DIRECTORY, 'patterns')
PATTERNS_TXT_FILE = path.join(PATTERNS_OUTPUT_DIRECTORY, 'all_patterns.txt')


def initialize_logger():
    root = log.getLogger()
    root.setLevel(log.DEBUG)

    ch = log.StreamHandler(sys.stdout)
    ch.setLevel(log.DEBUG)
    root.addHandler(ch)


def main():
    if len(sys.argv) < 2:
        print('Need number of points')
        exit(1)

    initialize_logger()

    points = int(sys.argv[1])
    log.info('Starting to look for patterns on {0} points'.format(points))
    matchings = enumerate_matchings(points)
    log.info("Finished enumerating matchings, found {0}".format(len(matchings)))
    found_patterns = list(enumerate_patterns(matchings))
    log.info("Finished looking for patterns, found {0}".format(len(found_patterns)))
    found_patterns = deduplicate_patterns(found_patterns)
    log.info("Finished deduplicating patterns, found {0}".format(len(found_patterns)))
    pattern_dumper = PatternDumper(OUTPUT_RESULT_DIRECTORY)
    pattern_dumper.dump_all_patterns(found_patterns)
    pattern_dumper.dump_separate_patterns(found_patterns, points)


if __name__ == '__main__':
    main()