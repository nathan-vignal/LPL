import copy
class Corpus():

    def __init__(self,type,path,name):
        Corpus.delimiters = {'CID': ' ', 'DVD': ',', 'MTX': ',', 'SWBD': ' '}
        self.__name = name
        self.__type = type
        self.__path = path
        self.__elements = []
        self.__nbOfLines = 0
        self.__numberOfLinesByFile =[]
        self.__durationByFile = []
        self.__numberOfWordsByFile = []
        if type in Corpus.delimiters.keys():
            self.delimiter = Corpus.delimiters[type]
        else:
            if type == 'Fisher':
                self.delimiter = ""
            else:
                print("wrong type : " + type)

    def addElements(self, elements):
        '''
        add the content of elements inside the corpus's group of file
        :param elements: is a file containing a written oral interaction
        '''
        for element in elements:
            self.__elements.append(element)

    def getNumberOfFiles(self):
        return len(self.__elements)

    def getNbOfLines(self):
        """
         calculate __nbOfLines it if it's not already done and return it
        :return: __nbOfLines
        """
        if self.__nbOfLines == 0:
            for file in self.__elements:
                self.__nbOfLines += file.getNbOfLines()
        return copy.copy(self.__nbOfLines)

    def getNbOfLinesByFile(self):
        """
         calculate __numberOfLinesByFile it if it's not already done and return it
        :return: __numberOfLinesByFile
        """
        if self.__numberOfLinesByFile == []:
            for file in self.__elements:
                self.__numberOfLinesByFile.append(file.getNbOfLines())
        return copy.copy(self.__numberOfLinesByFile)



    def getDurationByFile(self):
        """
         calculate __durationByFile it if it's not already done and return it
        :return: __durationByFile
        """
        if self.__durationByFile == []:
            for file in self.__elements:
                self.__durationByFile.append(file.getDuration())
        return copy.copy(self.__durationByFile)

    def getNumberOfWordsByFile(self):
        """
        calculate __numberOfWordsByFile it if it's not already done and return it
        :return: __numberOfWordsByFile
        """
        if self.__numberOfWordsByFile == []:
            for file in self.__elements:
                self.__numberOfWordsByFile.append(file.getNbWords())
        return copy.copy(self.__numberOfWordsByFile)

    def getName(self):
        return copy.copy(self.__name)

    def getSpeakerByFile(self):
        if self.__name != "SWBD":
            print("no speakers for"+self.__name)
            return
        speakers = []
        for file in self.__elements:
            speakers.append(file.getSpeaker())
        return speakers

