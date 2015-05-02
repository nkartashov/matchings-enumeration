__author__ = 'nikita_kartashov'

from collections import defaultdict


class CacheScorer(object):
    def __init__(self):
        self._cached_results = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

    def retrieve(self, cls, input_left, input_right):
        if input_left > input_right:
            input_left, input_right = input_right, input_left
            return self._cached_results[cls][input_left][input_right]

    def add(self, cls, input_left, input_right, value):
        if input_left > input_right:
            input_left, input_right = input_right, input_left
        self._cached_results[cls][input_left][input_right] = value