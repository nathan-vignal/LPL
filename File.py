import csv
class File():

    def __init__(self,path,delimiter):
        self.delimiter = delimiter
        self.path = path
        self.__nbOfLines = 0


    def getNbOfLines(self):
        if self.__nbOfLines == 0:
            with open(self.path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    line_count += 1
        self.__nbOfLines = line_count
        return self.__nbOfLines
