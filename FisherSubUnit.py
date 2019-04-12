import copy
import math

class FisherSubUnit:


    def __init__(self, father, speakerId):
        self.__father = father
        self.__nbOfLines = 0
        self.__numberOfWords = 0
        self.__speakerId = speakerId

        # all the getters are in charge for initilazing a vairable if it's not yet initialized yet and then return it


    def getNbOfLines(self):

        if self.__nbOfLines == 0:
            self.initVariables()
        return copy.copy(self.__nbOfLines)

    def getDuration(self):
        raise ValueError('getDuration not yet implemented in FisherSubUnit.py')

    def getNbWords(self):
        if self.__numberOfWords == 0:
            self.initVariables()
        return copy.copy(self.__numberOfWords)

    def initVariables(self):
        self.__numberOfWords = 0 # we only use += on this variable so this is for safety
        f1 = open(self.__father.getpath() + self.__father.getidFile() + ".TRN", "r")
        lines = f1.readlines()
        if self.__speakerId == "B":
            i=1
            while self.__speakerId == lines[-i].split("-")[-2]:
                self.__numberOfWords += lines[-i].count(' ') - 1
                i += 1
            self.__nbOfLines = i
        else:
            i=0
            while self.__speakerId == lines[i].split("-")[-2]:
                self.__numberOfWords += lines[i].count(' ') - 1
                i += 1
            self.__nbOfLines = i
        f1.close()


