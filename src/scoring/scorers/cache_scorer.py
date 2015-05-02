__author__ = 'nikita_kartashov'


class CacheScorer(object):
    def __init__(self, size, possible_keys):
        self._cached_results = dict()
        for key in possible_keys:
            self._cached_results[key] = [[0 for _ in range(size)] for _ in range(size)]

    def retrieve(self, cls, input_left, input_right):
        if input_left > input_right:
            input_left, input_right = input_right, input_left
        return self._cached_results[cls][input_left][input_right]

    def add(self, cls, input_left, input_right, value):
        if input_left > input_right:
            input_left, input_right = input_right, input_left
        self._cached_results[cls][input_left][input_right] = value