from os import path
from ..pathManagment import getTextPath
from copy import copy

class UselessWords:
    def __init__(self):
        file = open(path.join(getTextPath(), "bannedWords"), "r")
        self.__myWords = file.readlines()[0].split(' ')

    def get(self):
        return copy(self.__myWords)


