from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.glyphs import VBar
import numpy as np
import RadarGraph
from bokeh.models.annotations import Title
from bokeh.plotting import figure
from bokeh.io import show, push_notebook
import math
import copy
class RadarModel:

    def __init__(self, corpus, input, graph):
        self.__corpus = corpus
        self.__corpusToAnalyzeNames = "*"
        self.__associatedInputs = [input]
        self.__corpusAnalysis = {}
        self.__corpusColor = {}
        self.__graph = graph
        colors = ["black", "blue", "red", "yellow", "green"
                , "purple", "white", "brown", "orange", "pink"]
        if len(corpus) > len(colors):
            colors.extend(["black"] * (len(corpus)-len(colors)))
        for i in range(0, len(corpus)):
            self.__corpusColor[corpus[i].getName()] = colors[i]

        #  printing each color associated with each corpus
        for i in range(0, len(self.__corpus)):
            print(self.__corpus[i].getName() + " : " + colors[i])

        input.observe(self)
        self.refreshInputInfos()



    def __call__(self, *args):
        """
        used to refresh the infos of the model
        :param args:
        :return:
        """
        self.refreshInputInfos()
        if self.__corpusToAnalyzeNames != []:
            self.analyseCorpus()





    def refreshInputInfos(self):
        """
        refresh the attributes by checking the inputs the model contains
        :return:
        """

        for input in self.__associatedInputs:
            dataType = input.getDataType()
            if dataType == "discrimination":
                self.__discriminationCriterion = input.getValue()
            elif dataType == "corpusNames":
                self.__corpusToAnalyzeNames = input.getValue()
            elif dataType == "analysisFunction":
                self.__typeOfAnalysis = input.getValue()
            else:
                print("unrecognized data type" + input.getDataType())

    def getCorpusToAnalyse(self):
        toReturn = []
        for corpus in self.__corpus:
            if corpus.getName() in self.__corpusToAnalyzeNames:
                toReturn.append(corpus)
        return toReturn

    def analyseCorpus(self):

        corpusToAnalyse = self.getCorpusToAnalyse()
        # getting the data to display
        for corpus in corpusToAnalyse:
            if corpus.getName() in self.__corpusAnalysis:
                continue

            temp = []
            temp.append(corpus.getMeanLexicalRichness())
            nbWords = corpus.getMeanNumberOfWords()

            if corpus.getName() in "SWBD Fisher":
                if nbWords != 0:
                    temp.append(
                        corpus.countSpecialWords(open("./corpusRelated/txt/fill_en", "r").readlines()[0].split(',')
                                                 ) / float(nbWords))
                else:
                    temp.append(0)
                temp.append(corpus.getRatioSpecialIpu("feedback_en"))
                temp.append(corpus.getSpecialIpuMeanSize("not feedback_en"))
                nbSpecialWords = corpus.countSpecialWords(["yes"])
                if nbSpecialWords != 0:

                    yeah = corpus.countSpecialWords(["yeah"])
                    temp.append(yeah / float(nbSpecialWords))
                else:
                    temp.append(0)

            else:
                if nbWords != 0:

                    nbSpecialWords = corpus.countSpecialWords(open("./corpusRelated/txt/fill_fr", "r").readlines()[0].split(',')
                                                 )
                    temp.append(nbSpecialWords / float(nbWords))

                else:
                    temp.append(0)

                temp.append(corpus.getRatioSpecialIpu("feedback_fr"))
                temp.append(corpus.getSpecialIpuMeanSize("not feedback_fr"))

                nbSpecialWords = corpus.countSpecialWords(["oui"])
                if nbSpecialWords != 0:
                    temp.append(corpus.countSpecialWords(["ouais"]) / nbSpecialWords)
                else:
                    temp.append(0)
            self.__corpusAnalysis[corpus.getName()] = temp

        data = []
        for corpus in corpusToAnalyse:
            data.append(copy.copy(self.__corpusAnalysis[corpus.getName()]))


        #  setting all values in ratio with 1 being the max value
        maxUniqueNbWords = [0] * (len(data[0]))

        for item in data:
            for i in range(0, len(item)):
                if item[i] > maxUniqueNbWords[i]:
                    maxUniqueNbWords[i] = item[i]
        for item in data:
            for i in range(0, len(item)):

                if maxUniqueNbWords[i] != 0:
                    item[i] = item[i] / float(maxUniqueNbWords[i])
                else:
                    print(" maxUniqueWords = 0")

        #  pass the data in np.array
        npData = []
        for i in range(0, len(data)):
            npData.append(np.array(data[i]))

        #  getting the associated colors with the right corpus
        colors = []
        for corpus in corpusToAnalyse:
            colors.append(self.__corpusColor[corpus.getName()])



        #  creating the title of each axis onn the graph
        text = ["richesse lexicale",
                "ratio fill",
                "ratio feedback",
                "taille moyenne Ipu non feedback",
                "yeah/yes"]
        for i in range(0, len(text)):
            text[i] += " max :" + '%.3f' % (maxUniqueNbWords[i])

        self.__graph.createRadarGraph(text, npData, colors=colors)
        self.__graph.update()




