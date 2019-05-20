import copy
from nltk.probability import FreqDist

class FisherSubUnit:

    def __init__(self, father, speakerId):
        self.__father = father
        self.__nbOfLines = None
        self.__numberOfWords = None
        self.__speakerId = speakerId
        self.__nbUniqueWords = None
        self.__distFrequency = None

        # all the getters are in charge for initilazing a vairable if it's not yet initialized yet and then return it

    def getNbOfLines(self):

        if self.__nbOfLines == None:
            self.initVariables()
        return copy.copy(self.__nbOfLines)

    def getDuration(self):
        return 0 #no duraton for fisher yet !

    def getNbWords(self):
        if self.__numberOfWords == None:
            self.initVariables()
        return copy.copy(self.__numberOfWords)

    def initVariables(self):
        lines = self.getLines()
        self.__numberOfWords = 0
        wordsSet = set()
        for line in lines:
            self.__numberOfWords += line.count(' ') - 2
            for word in line.split(' ')[0:-2]:
                wordsSet.add(word)
        self.__nbOfLines = len(lines)
        self.__nbUniqueWords = len(wordsSet)



    def getRatioSpecialIpu(self, fctAnalyseIpu):
        lines = self.getLines()
        nbSpecialIpu = 0
        for line in lines:
            if fctAnalyseIpu(line.split(' ')[0:-2]):
                nbSpecialIpu += 1
        if self.getNbOfLines() == 0:
            print("no lines found")
            return 0
        return nbSpecialIpu / float(self.getNbOfLines())

    def getNbSpecialIpu(self, fctAnalyseIpu):
        lines = self.getLines()
        nbSpecialIpu = 0
        for line in lines:
            if fctAnalyseIpu(line.split(' ')[0:-2]):
                nbSpecialIpu += 1
        if self.getNbOfLines() == 0:
            print("no lines found")
            return 0
        return nbSpecialIpu

    def getNbUniqueWords(self):
        if self.__nbUniqueWords == None:
            self.initVariables()
        return copy.copy(self.__nbUniqueWords)

    def getMeanSizeSpecialIpu(self, fctAnalyseIpu):

        lines = self.getLines()
        nbSpecialIpu = 0
        meanSizeSpecialIpu = 0
        for line in lines:
            words = line.split(' ')[0:-2]
            if fctAnalyseIpu(words):
                nbSpecialIpu += 1
                meanSizeSpecialIpu += len(words)
        if self.getNbOfLines() == 0:
            print("no lines found")
            return 0
        if nbSpecialIpu == 0:
            return 0
        return meanSizeSpecialIpu / float(nbSpecialIpu)

    def countSpecialWords(self, specialWords):
        lines = self.getLines()
        nbOccurence = 0
        for line in lines:
            words = line.split(' ')[0:-2]
            for word in words:
                if word.replace("\n", "").lower() in specialWords:
                    nbOccurence += 1
        return nbOccurence

    def getLines(self):
        """
        care for if speaker id is b the lines will be returned from the last to the first
        :return:
        """
        f = open(self.__father.getpath() + self.__father.getidFile() + ".TRN", "r")
        lines = f.readlines()
        subUnitLines = []

        if self.__speakerId == "A":
            for line in lines:
                if self.__speakerId == line.split("-")[-2]:
                    subUnitLines.append(line)
        elif self.__speakerId == "B":
            for line in reversed(lines):
                if self.__speakerId == line.split("-")[-2]:
                    subUnitLines.append(line)

        f.close()
        return subUnitLines

    def distFrequency(self):
        if self.__distFrequency is None:
            lines = self.getLines()
            arrayDistFrequency = []
            for line in lines:
                arrayDistFrequency.append(FreqDist(word.lower() for word in line.split(' ')[0:-2]))

            self.__distFrequency = FreqDist()
            for distFrequency in arrayDistFrequency:
                self.__distFrequency += distFrequency
        return copy.copy(self.__distFrequency)





