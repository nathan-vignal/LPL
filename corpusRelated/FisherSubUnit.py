import copy


class FisherSubUnit:

    def __init__(self, father, speakerId):
        self.__father = father
        self.__nbOfLines = None
        self.__numberOfWords = None
        self.__speakerId = speakerId
        self.__nbUniqueWords = None

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
        self.__numberOfWords = 0
        f1 = open(self.__father.getpath() + self.__father.getidFile() + ".TRN", "r")
        lines = f1.readlines()
        wordsSet = set()
        if self.__speakerId == "B":
            i = 1
            while self.__speakerId == lines[-i].split("-")[-2]:
                self.__numberOfWords += lines[-i].count(' ') - 2
                for word in lines[-i].split(' ')[0:-2]:
                    wordsSet.add(word)
                i += 1
            self.__nbOfLines = i
        else:
            i = 0
            while self.__speakerId == lines[i].split("-")[-2]:
                self.__numberOfWords += lines[i].count(' ') - 2
                i += 1
            self.__nbOfLines = i
        f1.close()
        self.__nbUniqueWords = len(wordsSet)

    def getRatioSpecialIpu(self, fctAnalyseIpu):
        f1 = open(self.__father.getpath() + self.__father.getidFile() + ".TRN", "r")
        lines = f1.readlines()
        nbSpecialIpu = 0
        for line in lines:
            if fctAnalyseIpu(line.split(' ')[0:-2]):
                nbSpecialIpu += 1
        if self.getNbOfLines() == 0:
            print("returning 0")
            return 0
        return nbSpecialIpu / float(self.getNbOfLines())

    def getNbSpecialIpu(self, fctAnalyseIpu):
        f1 = open(self.__father.getpath() + self.__father.getidFile() + ".TRN", "r")
        lines = f1.readlines()
        nbSpecialIpu = 0
        for line in lines:
            if fctAnalyseIpu(line.split(' ')[0:-2]):
                nbSpecialIpu += 1
        if self.getNbOfLines() == 0:
            print("returning 0")
            return 0
        return nbSpecialIpu

    def getNbUniqueWords(self):
        if self.__nbUniqueWords == None:
            self.initVariables()
        return copy.copy(self.__nbUniqueWords)

    def getMeanSizeSpecialIpu(self, fctAnalyseIpu):

        f1 = open(self.__father.getpath() + self.__father.getidFile() + ".TRN", "r")
        lines = f1.readlines()
        nbSpecialIpu = 0
        meanSizeSpecialIpu = 0
        for line in lines:
            words = line.split(' ')[0:-2]
            if fctAnalyseIpu(words):
                nbSpecialIpu += 1
                meanSizeSpecialIpu += len(words)
        if self.getNbOfLines() == 0:
            print("returning 0")
            return 0
        if nbSpecialIpu == 0:
            return 0
        return meanSizeSpecialIpu / float(nbSpecialIpu)

    def countSpecialWords(self, specialWords):
        f1 = open(self.__father.getpath() + self.__father.getidFile() + ".TRN", "r")
        lines = f1.readlines()
        nbOccurence = 0
        for line in lines:
            words = line.split(' ')[0:-2]
            for word in words:
                if word.replace("\n", "").lower() in specialWords:
                    nbOccurence += 1
        return nbOccurence
