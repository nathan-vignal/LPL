import copy
from corpusRelated.Ipu import *
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

class Corpus():
    """
    represent a corpus in the program
    """

    def __init__(self, type, path, name):
        """

        :param type: type of the corpus will determine what delimiter is used
        :param path: str path to the file
        :param name: name of the corpus
        """
        Corpus.delimiters = {'CID': ' ', 'DVD': ',', 'MTX': ',', 'SWBD': ' '}
        self.__name = name
        self.__type = type
        self.__path = path
        self.__files = []
        self.__nbOfLines = 0
        self.__numberOfLinesByFile = []
        self.__durationByFile = []
        self.__numberOfWords = None
        self.__numberOfWordsByFile = []
        if type in Corpus.delimiters.keys():
            self.delimiter = Corpus.delimiters[type]
        else:
            if type == 'Fisher':
                self.delimiter = ""
            else:
                print("wrong type : " + type)

    def addElements(self, elements):
        """
        add the content of elements inside the corpus's group of file
        :param elements: is a file containing a written oral interaction
        """
        for element in elements:
            self.__files.append(element)

    def getNumberOfFiles(self):
        return len(self.__files)

    def getNbOfLines(self):
        """
         calculate __nbOfLines it if it's not already done and return it
        :return: __nbOfLines
        """
        if self.__nbOfLines == 0:
            for file in self.__files:
                self.__nbOfLines += file.getNbOfLines()
        return copy.copy(self.__nbOfLines)

    def getNbOfLinesByFile(self):
        """
         calculate __numberOfLinesByFile it if it's not already done and return it
        :return: __numberOfLinesByFile
        """
        if self.__numberOfLinesByFile == []:
            for file in self.__files:
                self.__numberOfLinesByFile.append(file.getNbOfLines())
        return copy.copy(self.__numberOfLinesByFile)



    def getDurationByFile(self):
        """
         calculate __durationByFile it if it's not already done and return it
        :return: __durationByFile
        """
        if self.__durationByFile == []:
            for file in self.__files:
                self.__durationByFile.append(file.getDuration())
        return copy.copy(self.__durationByFile)

    def getNumberOfWordsByFile(self):
        """
        calculate __numberOfWordsByFile it if it's not already done and return it
        :return: __numberOfWordsByFile
        """
        if self.__numberOfWordsByFile == []:
            for file in self.__files:
                self.__numberOfWordsByFile.append(file.getNbWords())
        return copy.copy(self.__numberOfWordsByFile)

    def getNumberOfWords(self):
        if self.__numberOfWords is None:
            sum = 0

            for file in self.__files:
                sum += file.getNbWords()
            self.__numberOfWords = sum
        return self.__numberOfWords

    def getName(self):
        return copy.copy(self.__name)

    def getSpeakerByFile(self):
        if self.__name != "SWBD":
            print("no speakers for"+self.__name)
            return
        speakers = []
        for file in self.__files:
            speakers.append(file.getSpeaker())
        return speakers

    def getNbOfFiles(self):
        return len(self.__files)

    def getRatioSpecialIpu(self, ipuType):

        fct = stringToIpuFct(ipuType)

        if fct is None:
            print("unknow ipuType in Corpus.py getNbSpecialIPu")
            return -1
        mean = 0
        for file in self.__files:
            mean += file.getRatioSpecialIpu(fct)
        return mean / len(self.__files)

    def getSpecialIpuMeanSize(self, ipuType):
        fct = stringToIpuFct(ipuType)
        if fct is None:
            print("unknow ipuType in Corpus.py getNbSpecialIPu")
            return -1
        mean = 0
        for file in self.__files:
            mean += file.getMeanSizeSpecialIpu(fct)
        return mean / float(len(self.__files))


    def getMeanNbUniqueWords(self):
        mean = 0
        for file in self.__files:
            mean += file.getNbUniqueWords()
        return mean / len(self.__files)

    def getMeanLexicalRichness(self):
        mean = 0
        for file in self.__files:
            nbWords = file.getNbWords()
            if nbWords != 0:
                 mean += file.getNbUniqueWords() / float(nbWords)
        return mean / len(self.__files)

    def countSpecialWords(self, specialWords):
        mean = 0
        for file in self.__files:
            mean += file.countSpecialWords(specialWords)
        return mean / float(len(self.__files))

    def distFrequency(self):

        sum = FreqDist()
        for file in self.__files:
            sum += file.distFrequency()
            print("one more")
        return sum




