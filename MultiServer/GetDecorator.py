from typing import Any
from GetHandler import GetHandler


class GET():
    def __init__(self, path):
        self.path = path
    def __call__(self, func):
        handler = GetHandler()
        self.func = func
        handler.add_routes(self.path, self.func)
        return func
