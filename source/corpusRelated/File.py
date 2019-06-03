import copy
import math
from nltk.probability import FreqDist
import io
from os import path
from source.pathManagment import getTextPath

class File:

    def __init__(self, path, corpus):
        self.__corpus = corpus
        self.path = path
        self.__nbOfLines = 0
        self.__duration = 0
        self.__numberOfWords = 0
        self.__numberUniqueWords = 0
        self.__distFreq = None
        self.__specialDistrFreq = {}
        self.initProperties()

    def initProperties(self):

        file = open(path.join(getTextPath(),"bannedWords"), "r")
        notInterrestingWords = file.readline(1)[0].split(' ')
        lines = self.getLines()
        self.__duration = math.floor(
            float(lines[-1].split(self.__corpus.getDelimiter())[2]) - float(lines[0].split(self.__corpus.getDelimiter())[1]))  # init duration


        uniqueWords = set()

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
        lines = self.getLines()

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
        lines = self.getLines()

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
        lines = self.getLines()

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

        lines = self.getLines()
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
            splitted = item.split(self.__corpus.getContentDelimiter())  # this should be enough
                                                                        # but CID contains 2 delimiters
            for word in splitted:
                words.extend(word.split("_"))  # specific to CID
        if "" in words:
            words.remove("")  # debug some corpus

        uselesWords = self.__corpus.getUselessWords()
        #print(uselesWords) # debug
        for uselessWord in uselesWords:
            for contentWord in words:
                if contentWord == uselessWord:

                    words.remove(contentWord)

        return words

    def distFrequency(self):
        """
        generate a distribution frequency of words for this file
        :return:
        """
        file = open(path.join(getTextPath(), "bannedWords"), "r")
        notInterrestingWords = file.readline(1)[0].split(' ')
        if self.__distFreq is None:
            lines = self.getLines()
            arrayDistFrequency = []
            for line in lines:
                words = [word.lower() for word in self.readIpu(line)]
                for word in notInterrestingWords:
                    if word in words:
                        words.remove(word)

                arrayDistFrequency.append(FreqDist(words))

            sum = FreqDist()
            for distFrequency in arrayDistFrequency:
                sum += distFrequency

            self.__distFreq = sum

        return self.__distFreq

    def getShortIpuDistFreq(self):
        """
        get the distribution frequency of words used in all short IPUs
        :return:
        """

        if "shortIpu" not in self.__specialDistrFreq:
            lines = self.getLines()
            arrayDistFrequency = []

            for line in lines:
                words = self.readIpu(line)
                if len(words) < 4:
                    arrayDistFrequency.append(FreqDist(word.lower() for word in words))

            sum = FreqDist()
            for distFrequency in arrayDistFrequency:
                sum += distFrequency

            self.__specialDistrFreq["shortIpu"] = sum
        return self.__specialDistrFreq["shortIpu"]



    def getLongIpuDistFreq(self):
        """
        get all the first and the last word of long(more than 3 words) IPU and return them as a frequency distribution
        :return:
        """
        if "longIpuStart" not in self.__specialDistrFreq or "longIpuEnd" not in self.__specialDistrFreq:
            lines = self.getLines()
            arrayStartWords = []
            arrayEndWords = []

            for line in lines:
                words = self.readIpu(line)
                if len(words) > 3:
                    arrayStartWords.append(words[0])
                    arrayEndWords.append(words[-1])

            freqStart = FreqDist(arrayStartWords)
            freqEnd = FreqDist(arrayEndWords)

            self.__specialDistrFreq["longIpuStart"] = freqStart
            self.__specialDistrFreq["longIpuEnd"] = freqEnd

        return self.__specialDistrFreq["longIpuStart"], self.__specialDistrFreq["longIpuEnd"]

    def getLines(self):
        file = open(self.path, "r")
        lines = file.readlines()
        file.close()
        return lines















