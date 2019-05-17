import copy
import math
from nltk.probability import FreqDist
import io

class File:



    def __init__(self, path, corpus):
        self.__corpus = corpus
        self.path = path
        self.__nbOfLines = 0
        self.__duration = 0
        self.__numberOfWords = 0
        self.__numberUniqueWords = 0
        self.initProperties()

    def initProperties(self):

        file = open("./corpusRelated/txt/bannedWords", "r")
        notInterrestingWords = file.readline(1)[0].split(' ')
        f1 = open(self.path, "r")
        lines = f1.readlines()
        self.__duration = math.floor(
            float(lines[-1].split(self.__corpus.getDelimiter())[2]) - float(lines[0].split(self.__corpus.getDelimiter())[1]))  # init duration


        uniqueWords = set()
        self.__distFreq = None

        for line in lines:
            self.__nbOfLines += 1

            words = self.readIpu(line)
            for word in words:
                if word not in notInterrestingWords:
                    self.__numberOfWords += len(word.split('_'))
                    uniqueWords.add(word)
        self.__numberUniqueWords = len(uniqueWords)

# all the getters are in charge for initilazing a vairable if it's not yet initialized yet and then return it


    def getNbOfLines(self):
        return copy.copy(self.__nbOfLines)

    def getDuration(self):
        """

        :return: __duration
        """
        return copy.copy(self.__duration)


    def getNbWords(self):
        """
        :return: __numberOfWords
        """
        return copy.copy(self.__numberOfWords)

    def getNbUniqueWords(self):
        """
        :return: (int) __numberUniqueWords
        """
        return copy.copy(self.__numberUniqueWords)

    def getRatioSpecialIpu(self, fctAnalyseIpu):
        """
        go throught all the file and get the ratio special ipu/all ipu
        :param fctAnalyseIpu: function that will check if a IPU is special
        :return:
        """
        f1 = open(self.path, "r")
        lines = f1.readlines()

        nbSpecialIpu = 0
        for line in lines:

            if fctAnalyseIpu(self.readIpu(line)):
                nbSpecialIpu += 1

        return nbSpecialIpu/float(self.__nbOfLines)

    def getNbSpecialIpu(self, fctAnalyseIpu):
        """
                go throught all the file and get the nb of special ipu(the ones that trigger fctAnalyseIpu)
                :param fctAnalyseIpu: function that will check if a IPU is special
                :return:
                """
        f1 = open(self.path, "r")
        lines = f1.readlines()

        nbSpecialIpu = 0
        for line in lines:
            words = self.readIpu(line)
            if fctAnalyseIpu(words):
                nbSpecialIpu += 1
        return nbSpecialIpu

    def getMeanSizeSpecialIpu(self, fctAnalyseIpu):
        """
        go throught all the file and get the mean size of the special ipu(the ones that trigger fctAnalyseIpu)
        :param fctAnalyseIpu: function that will check if a IPU is special
        :return:
        """
        f1 = open(self.path, "r")
        lines = f1.readlines()

        specialIpuMeanSize = 0
        nbSpecialIpu = 0
        for line in lines:
            words = self.readIpu(line)
            if fctAnalyseIpu(words):
                nbSpecialIpu += 1
                specialIpuMeanSize += len(words)

        if nbSpecialIpu == 0:
            return 0

        return specialIpuMeanSize / float(nbSpecialIpu)

    def countSpecialWords(self, specialWords):
        """

        :param specialWords: [string] words to count in the file
        :return: number of time the words are contained in the file, words can be present independently
        """
        if not isinstance(specialWords, list):
            raise TypeError("expected a list ")
        if not isinstance(specialWords[0], str):
            print("expected a list of string in File.py countSpecialWords")

        f1 = open(self.path, "r")
        lines = f1.readlines()
        nbOfOccurrence = 0
        for line in lines:
            words = self.readIpu(line)
            for word in words:
                if word in specialWords:
                    nbOfOccurrence += 1
        return nbOfOccurrence

    def readIpu(self, content):

        if not isinstance(content, str):
            raise TypeError(content)

        content = content.replace("\n", "").lower()
        content = content.split(self.__corpus.getDelimiter())

        end = self.__corpus.getIndexEndContent()
        if self.__corpus.getIndexEndContent() == "last":
            end = len(content)

        content = content[self.__corpus.getIndexStartContent():end]
        words = []
        for item in content:
            words.extend(item.split(self.__corpus.getContentDelimiter()))
        return words




    def distFrequency(self):
        """
        generate a disctribution frequency of words for this file
        :return:
        """
        if self.__distFreq is None:
            f1 = open(self.path, "r")
            lines = f1.readlines()
            arrayDistFrequency = []
            for line in lines:

                arrayDistFrequency.append(FreqDist(word.lower() for word in self.readIpu(line)))

            sum = FreqDist()
            for distFrequency in arrayDistFrequency:
                sum += distFrequency

            self.__distFreq = sum

        return self.__distFreq















