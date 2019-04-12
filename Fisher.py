import copy
import math
import FisherSubUnit

class Fisher:

    def __init__(self, pathToDirectory, idFile):
        self.__path = pathToDirectory
        self.__idFile = idFile
        self.__duration = 0
        self.__nbOfLines = 0
        self.__numberOfWords = 0
        self.__nbOfLinesBySpeaker = []
        self.__numberOfWordsBySpeaker = []
        self.__sonA = FisherSubUnit.FisherSubUnit(self, "A")
        self.__sonB = FisherSubUnit.FisherSubUnit(self, "B")

    # standart getters
    def getidFile(self):
        """

        :return: string
        """
        return copy.copy(self.__idFile)

    def getpath(self):
        """

        :return: string
        """
        return copy.copy(self.__path)

    # special getters are in charge for initilazing a vairable if it's not yet initialized yet and then return it
    def getNbOfLinesBySpeaker(self):
        """

        :return: array of int
        """
        if self.__nbOfLinesBySpeaker == []:
            self.__nbOfLinesBySpeaker = [self.__sonA.getNbOfLines(), self.__sonB.getNbOfLines()]
        return copy.copy(self.__nbOfLinesBySpeaker)

    def getNbOfLines(self):
        """

        :return: int
        """
        if self.__nbOfLines == 0:
            self.__nbOfLines = self.__sonA.getNbOfLines() + self.__sonB.getNbOfLines()
        return copy.copy(self.__nbOfLines)

    def getNbWordsBySpeaker(self):
        """

        :return: array of int
        """
        if self.__numberOfWordsBySpeaker == []:
            self.__numberOfWordsBySpeaker = [self.__sonA.getNbWords(), self.__sonB.getNbWords()]
        return copy.copy(self.__numberOfWordsBySpeaker)

    def getNbWords(self):
        """

        :return:  int
        """
        if self.__numberOfWords == 0:
            self.__numberOfWords = self.__sonA.getNbWords() + self.__sonB.getNbWords()
        return copy.copy(self.__numberOfWords)


    def getDuration(self):
        return 0










