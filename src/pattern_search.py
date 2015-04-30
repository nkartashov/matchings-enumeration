__author__ = 'nikita_kartashov'

import sys
from os import path, makedirs

from .matchings import enumerate_matchings
from .pattern_enumeration import enumerate_patterns
from .pattern_deduplication import deduplicate_patterns
from .pattern_dumper import PatternDumper


OUTPUT_RESULT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '../result'))
PATTERNS_OUTPUT_DIRECTORY = path.join(OUTPUT_RESULT_DIRECTORY, 'patterns')
PATTERNS_TXT_FILE = path.join(PATTERNS_OUTPUT_DIRECTORY, 'all_patterns.txt')


def prepare_for_output():
    makedirs(PATTERNS_OUTPUT_DIRECTORY, exist_ok=True)


def main():
    if len(sys.argv) < 2:
        print('Need number of points')
        exit(1)

    points = int(sys.argv[1])
    matchings = enumerate_matchings(points)
    prepare_for_output()
    found_patterns = list(enumerate_patterns(matchings))
    found_patterns = deduplicate_patterns(found_patterns)
    pattern_dumper = PatternDumper(OUTPUT_RESULT_DIRECTORY)
    pattern_dumper.dump_all_patterns(found_patterns)
    pattern_dumper.dump_separate_patterns(found_patterns, points)


if __name__ == '__main__':
    main()