import time

class SnapchatCache:

    _lifespan = 2

    _cache = {}

    def get(self, key):
        if key not in self._cache:
            return None

        if self._cache[key]['time'] < time.time() - self._lifespan:
            return None

        return self._cache[key]['data']

    def set(self, key, data):
        self._cache[key] = {
            'time': time.time(),
            'data': data
        }
