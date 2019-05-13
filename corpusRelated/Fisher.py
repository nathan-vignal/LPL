from corpusRelated.FisherSubUnit import FisherSubUnit
import copy

class Fisher:

    def __init__(self, pathToDirectory, idFile):
        self.__path = pathToDirectory
        self.__idFile = idFile
        self.__duration = 0
        self.__nbOfLines = 0
        self.__numberOfWords = 0
        self.__nbOfLinesBySpeaker = []
        self.__numberOfWordsBySpeaker = []
        self.__sonA = FisherSubUnit(self, "A")
        self.__sonB = FisherSubUnit(self, "B")

    # standard getters
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

    def getNbUniqueWords(self):
        return (self.__sonA.getNbUniqueWords() + self.__sonB.getNbUniqueWords())/2

    def getRatioSpecialIpu(self, fctAnalyseIpu):

        return (self.__sonA.getRatioSpecialIpu(fctAnalyseIpu) + self.__sonB.getRatioSpecialIpu(fctAnalyseIpu))/float(2)

    def getNbSpecialIpu(self, fctAnalyseIpu):

        return (self.__sonA.getNbSpecialIpu(fctAnalyseIpu) + self.__sonB.getNbSpecialIpu(fctAnalyseIpu))/float(2)

    def getMeanSizeSpecialIpu(self, fctAnalyseIpu):
        return (self.__sonA.getMeanSizeSpecialIpu(fctAnalyseIpu) + self.__sonB.getMeanSizeSpecialIpu(fctAnalyseIpu)) / float(2)

    def countSpecialWords(self, specialWords):
        return (self.__sonA.countSpecialWords(specialWords) + self.__sonB.countSpecialWords(specialWords) )

    def getSons(self):
        return [self.__sonA, self.__sonB]
