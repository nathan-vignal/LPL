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
        self.__name = name
        self.__language = None
        self.__delimiter = None
        self.__indexStartContent = None
        self.__indexEndContent = None
        self.__contentDelimiter = None
        self.getCorpusInfo()
        self.__type = type
        self.__path = path
        self.__files = []
        self.__nbOfLines = 0
        self.__numberOfLinesByFile = None
        self.__durationByFile = []
        self.__numberOfWords = None
        self.__numberOfWordsByFile = None

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
        if self.__numberOfLinesByFile == None:
            self.__numberOfLinesByFile = []
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
        if self.__numberOfWordsByFile is None:
            self.__numberOfWordsByFile = []
            for file in self.__files:
                self.__numberOfWordsByFile.append(file.getNbWords())
        return copy.copy(self.__numberOfWordsByFile)

    def getMeanNumberOfWords(self, forEachFile = False):
        if self.__numberOfWords is None:

            if self.__numberOfWordsByFile is None:
                self.getNumberOfWordsByFile()

            self.__numberOfWords = sum(self.__numberOfWordsByFile)

        if forEachFile:
            return copy.copy(self.__numberOfWordsByFile)
        else:
            return self.__numberOfWords / len(self.__files)


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

    def getRatioSpecialIpu(self, ipuType, forEachFile = False):

        fct = stringToIpuFct(ipuType)
        if fct is None:
            print("unknow ipuType in Corpus.py getNbSpecialIPu")
            return -1
        temp = []
        for file in self.__files:
            temp.append(file.getRatioSpecialIpu(fct))
        if not forEachFile:
            return sum(temp) / float(len(self.__files))
        return temp

    def getSpecialIpuMeanSize(self, ipuType, forEachFile = False):
        fct = stringToIpuFct(ipuType)
        if fct is None:
            print("unknow ipuType in Corpus.py getNbSpecialIPu")
            return -1
        temp = []
        for file in self.__files:
            temp.append(file.getMeanSizeSpecialIpu(fct))
        if forEachFile == False:
            return sum(temp) / float(len(self.__files))
        return temp

    def getMeanNbUniqueWords(self, forEachFile = False):

        temp = []
        for file in self.__files:
            temp.append(file.getNbUniqueWords())
        if forEachFile == False:
            return sum(temp) / float(len(self.__files))
        return temp

    def getMeanLexicalRichness(self, forEachFile = False):

        temp = []
        for file in self.__files:
            nbWords = file.getNbWords()
            if nbWords == 0:
                temp.append(0)
            else:
                temp.append(file.getNbUniqueWords() / float(nbWords))
        if forEachFile == False :
            return sum(temp) / float(len(self.__files))
        return temp

    def countSpecialWords(self, specialWords, forEachFile = False):
        temp = []
        for file in self.__files:
            temp.append(file.countSpecialWords(specialWords))

        if forEachFile == False:
            return sum(temp) / float(len(self.__files))
        return temp

    def distFrequency(self):

        sum = FreqDist()
        for file in self.__files:
            sum += file.distFrequency()
        return sum

    def getCorpusInfo(self):
        f1 = open("./corpusRelated/txt/CorpusInfo", "r")
        lines = f1.readlines()
        for line in lines:
            line = line.split("\ ")
            if line[0] == self.__name:
                line = line[1].split('\,')
                for info in line:

                    data = info.split('\:')
                    if data[0] == "language":
                        self.__language = data[1]
                    elif data [0] == "delimiter":
                        self.__delimiter = data[1]
                    elif data[0] == "contentDelimiter":
                        self.__contentDelimiter = data[1]
                    elif data[0] == "indexStartContent":
                        self.__indexStartContent = int(data[1])
                    elif data[0] == "indexEndContent":
                        if data[1].isdigit():
                            self.__indexEndContent = int(data[1])
                        else :
                            self.__indexEndContent = data[1]
                    else:
                        print('unknown corpus info' + data[0])
                return
        print("unknown corpus name" + self.__name)
        return

    def getName(self):
        if self.__name == None:
            print("self.__name not set")
        return copy.copy(self.__name)

    def getDelimiter(self):
        if self.__delimiter == None:
            print("self.__delimiter not set")
        return copy.copy(self.__delimiter)

    def getLanguage(self):
        if self.__language == None:
            print("self.__language not set")
        return copy.copy(self.__language)

    def getContentDelimiter(self):
        if self.__contentDelimiter == None:
            print("content delimiter not set")
        return copy.copy(self.__contentDelimiter)

    def getIndexStartContent(self):
        if self.__indexStartContent == None:
            print("self.__indexStartContent not set")
        return copy.copy(self.__indexStartContent)

    def getIndexEndContent(self):
        if self.__indexEndContent == None:
            print("self.__indexEndContent not set")
        return copy.copy(self.__indexEndContent)



