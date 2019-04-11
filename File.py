import copy
import math
class File():

    def __init__(self,path,delimiter):
        self.delimiter = delimiter
        self.path = path
        self.__nbOfLines = 0
        self.__duration = 0
        self.__numberOfWords =0
        self.duration = self.getDuration()

# all the getters are in charge for initilazing a vairable if it's not yet initialized yet and then return it


    def getNbOfLines(self):
        if self.__nbOfLines ==0:
            with open(self.path) as f:
                for i, l in enumerate(f):
                    pass
            self.__nbOfLines = i+1
        return copy.copy(self.__nbOfLines)

    def getDuration(self):
        """

        :return: __duration
        """
        if self.__duration == 0:
            f1 = open(self.path, "r")
            lines = f1.readlines()
            self.__duration = math.floor(float(lines[-1].split(self.delimiter)[2]) - float(lines[0].split(self.delimiter)[1]))
            f1.close()
        return copy.copy(self.__duration)


    def getNbWords(self):
        """
        initialize __numberOfWords and return the number of "spoken" word in this file
        :return: __numberOfWords
        """
        if self.__numberOfWords == 0:
            file = open("./bannedWords", "r")
            notInterrestingWords = file.readline(1)[0].split(' ')

            if "/CID/" in self.path:    # cid2_AB_- 0034.7741 0036.2541 le.petit.se.gratte
                f1 = open(self.path, "r")
                lines = f1.readlines()
                for line in lines:
                    words = line.split(self.delimiter)[3].split('.')

                    for word in words:
                        if word not in notInterrestingWords:

                            self.__numberOfWords += len(word.split('_'))
                return copy.copy(self.__numberOfWords)

            if "/SWBD/" in self.path:
                f1 = open(self.path, "r")
                lines = f1.readlines()
                for line in lines:
                    words = line.split(' ')
                    for i in range(3,len(words)):
                        if words[i] not in notInterrestingWords:
                            self.__numberOfWords += len(words[i].split('_'))
                return copy.copy(self.__numberOfWords)

            if any(x in self.path for x in (['/MTX/','/DVD/'])):
                f1 = open(self.path, "r")
                lines = f1.readlines()
                for line in lines:
                    for word in line.split(self.delimiter)[3].split(' '):
                        if word not in notInterrestingWords:
                            self.__numberOfWords += len(word.split('_'))
                return copy.copy(self.__numberOfWords)

            print("trouble reading the number of words getNbWords in "+self.path)
            return 0 # avoid program crashing
        return copy.copy(self.__numberOfWords)











