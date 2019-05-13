import copy
import math
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from collections import Counter

class File:

    def initProperties(self):

        file = open("./corpusRelated/txt/bannedWords", "r")
        notInterrestingWords = file.readline(1)[0].split(' ')
        f1 = open(self.path, "r")
        lines = f1.readlines()
        self.__duration = math.floor(
            float(lines[-1].split(self.delimiter)[2]) - float(lines[0].split(self.delimiter)[1]))  # init duration

        if "/CID/" in self.path:
            self.__corpusType = 1
        elif "/SWBD/" in self.path:
            self.__corpusType = 2
        elif any(x in self.path for x in (['/MTX/', '/DVD/'])):
            self.__corpusType = 3
        else:
            print("unknown filetype in File.initProperties")
            return
        uniqueWords = set()
        self.__distFreq = None

        if self.__corpusType == 1:  # eg: cid2_AB_- 0034.7741 0036.2541 le.petit.se.gratte
            for line in lines:
                self.__nbOfLines += 1
                words = line.split(self.delimiter)[3].split('.')
                for word in words:
                    if word not in notInterrestingWords:
                        self.__numberOfWords += len(word.split('_'))
                        uniqueWords.add(word)
        elif self.__corpusType == 2:   # eg: sw2001A-ms98-a-0002 0.977625 11.561375 hi um yeah
            for line in lines:
                self.__nbOfLines += 1
                words = line.split(' ')
                for i in range(3, len(words)):
                    if words[i] not in notInterrestingWords:
                        self.__numberOfWords += len(words[i].split('_'))
                        uniqueWords.add(words[i])
        elif self.__corpusType == 3:   # eg: DVD_AG_1,0031.5941,0032.9824,euh ouais ouais eventuellement
            for line in lines:
                self.__nbOfLines += 1
                for word in line.split(self.delimiter)[3].split(' '):
                    if word not in notInterrestingWords:
                        self.__numberOfWords += len(word.split('_'))
                        uniqueWords.add(word)

        self.__numberUniqueWords = len(uniqueWords)

    def __init__(self, path, delimiter):
        self.delimiter = delimiter
        self.path = path
        self.__nbOfLines = 0
        self.__duration = 0
        self.__numberOfWords = 0
        self.__numberUniqueWords = 0
        self.__corpusType = None
        self.initProperties()


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

        if self.__corpusType == 1:
            words = content.split(self.delimiter)[3].split('.')  # eg: cid2_AB_- 0034.7741 0036.2541 le.petit.se.gratte
            return words

        elif self.__corpusType == 2:
            words = content.split(' ')[3:]  # eg: sw2001A-ms98-a-0002 0.977625 11.561375 hi um yeah
            return words

        elif self.__corpusType == 3:
            words = content.split(self.delimiter)[3].split(' ')  # eg: DVD_AG_1,0031.5941,0032.9824,euh ouais ouais
            return words

        else:
            raise TypeError("unknown corpusType in file.py")


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
                arrayDistFrequency.append(FreqDist(word.lower() for word in word_tokenize(" ".join(self.readIpu(line)))))

            sum = FreqDist()
            for distFrequency in arrayDistFrequency:
                sum += distFrequency

            self.__distFreq = sum

        return self.__distFreq















