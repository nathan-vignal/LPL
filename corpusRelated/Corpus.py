import copy
from corpusRelated.Ipu import *
from nltk.probability import FreqDist

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
        self.__hasSpeaker = None
        self.getCorpusInfo()
        self.__type = type
        self.__path = path
        self.__files = []
        self.__nbOfLines = None
        self.__numberOfLinesByFile = None
        self.__durationByFile = []
        self.__numberOfWords = None
        self.__distFrequency = None


    def addElements(self, elements):
        """
        add the content of elements inside the corpus's group of file
        :param elements: is a file containing a written oral interaction
        """
        for element in elements:
            self.__files.append(element)

    def getNumberOfFiles(self):
        return len(self.__files)


    def getNbOfLines(self, forEachFile=False):
        """
         calculate __numberOfLinesByFile it if it's not already done and return it
        :return: __numberOfLinesByFile
        """
        if self.__numberOfLinesByFile == None or self.__nbOfLines is None:
            self.__numberOfLinesByFile = []
            for file in self.__files:
                self.__numberOfLinesByFile.append(file.getNbOfLines())
            self.__nbOfLines = sum(self.__numberOfLinesByFile)
        if forEachFile:
            return copy.copy(self.__numberOfLinesByFile)
        else:
            return copy.copy(self.__nbOfLines)




    def getDuration(self, forEachFile=False):
        """
         calculate __durationByFile it if it's not already done and return it
        :return: __durationByFile
        """
        if self.__durationByFile == []:
            for file in self.__files:
                self.__durationByFile.append(file.getDuration())
        if not forEachFile:
            return copy.copy(self.__durationByFile)
        else:
            return sum(self.__durationByFile)

    def getNumberOfWords(self,forEachFile=False):
        """
        calculate __numberOfWordsByFile it if it's not already done and return it
        :return: __numberOfWordsByFile
        """
        if self.__numberOfWordsByFile is None:
            self.__numberOfWordsByFile = []
            for file in self.__files:
                self.__numberOfWordsByFile.append(file.getNbWords())
            self.__numberOfWords = sum(self.__numberOfLinesByFile)
        if not forEachFile :
            return copy.copy(self.__numberOfWordsByFile)
        else:
            return self.__numberOfWords
    def getMeanNumberOfWords(self):
        """
        get the number of words in files
        :param forEachFile: if False mean the result else return a value for each file in an array
        :return:
        """
        if self.__numberOfWords is None:
            self.getNumberOfWords()

        return self.__numberOfWords / len(self.__files)

    def getSpeakerByFile(self):
        """
        get the speaker id for each file and return it in an array
        :return: [string]
        """
        if not self.__hasSpeaker:
            print("this corpus has no speaker according to corpus info")
        speakers = []
        for file in self.__files:
            speakers.append(file.getSpeaker())
        return speakers

    def getNbOfFiles(self):
        return len(self.__files)

    def getRatioSpecialIpu(self, ipuType, forEachFile = False):
        """
        search a function to read the ipuType
        :param ipuType: string
        :param forEachFile: bool
        :return: ratio of special IPU by file or in total
        """
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
        """
        get a special kind of IPU mean size(in number of words)
        :param ipuType: str see stringToIpuFct for more info
        :param forEachFile: if you want a value fo each file or a mean
        :return:
        """
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
        """
        get number of unique words in the files, by distinct value or by mean
        :param forEachFile:if you want a value fo each file or a mean
        :return:
        """

        temp = []
        for file in self.__files:
            temp.append(file.getNbUniqueWords())
        if forEachFile == False:
            return sum(temp) / float(len(self.__files))
        return temp

    def getMeanLexicalRichness(self, forEachFile = False):
        """
        get lexical richness by file or a mean over the corpus
        def lexical richness : number of unique words / number of total words
        :param forEachFile: if you want a value fo each file or a mean
        :return:
        """

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
        """
        count number of special words inside files
        :param specialWords:
        :param forEachFile:
        :return:
        """
        temp = []
        for file in self.__files:
            temp.append(file.countSpecialWords(specialWords))

        if forEachFile == False:
            return sum(temp) / float(len(self.__files))
        return temp

    def distFrequency(self):
        """
        create a dictionary with the number of time each word appear in the corpus
        :return: dict
        """
        if self.__distFrequency == None:
            self.__distFrequency = FreqDist()

            for file in self.__files:
                self.__distFrequency += file.distFrequency()
        return self.__distFrequency

    def getCorpusInfo(self):
        """
        search the corpus info file in order to get info on how to read the corpus it's files
        :return:
        """
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
                    elif data[0] == "speaker":
                        if data[1] == "on":
                            self.__hasSpeaker = True
                        elif data[1] == "off":
                            self.__hasSpeaker = False
                        else:
                            print("unknow speaker info")

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

    def getHasSpeaker(self):
        if self.__hasSpeaker == None:
            print("self.__hasSpeaker not set")
        return copy.copy(self.__hasSpeaker)




