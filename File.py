import csv
import math
class File():

    def __init__(self,path,delimiter):
        self.delimiter = delimiter
        self.path = path
        self.__nbOfLines = self.getNbOfLines()
        self.duration = self.getDuration()


    def getNbOfLines(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                line_count += 1
            return line_count

    def getDuration(self):
        f1 = open(self.path, "r")
        duration = f1.readlines()[-1].split(self.delimiter)[2]
        f1.close()
        return math.floor(float(duration))