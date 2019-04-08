class Corpus():

    def __init__(self,type,path,name):
        self.name = name
        Corpus.delimiters = {'CID': ' ', 'DVD': ',', 'MTX': ','}
        self.type = type
        self.path = path
        self.elements = []
        self.__nbOfLines =0
        if type in Corpus.delimiters.keys():
            self.delimiter = Corpus.delimiters[type]
        else :
            print("wrong type : "+ type )


    def addElements(self, elements):
        for element in elements:
            self.elements.append(element)

    def getNbOfLines(self):
        if self.__nbOfLines == 0:
            for file in self.elements:
                self.__nbOfLines += file.getNbOfLines()
        return self.__nbOfLines
    def getNumberOfFiles(self):
        return len(self.elements)
