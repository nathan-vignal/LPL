import pandas as pd
import numpy as np
import math
import copy
import math
from source.DimensionalityReduction import pca, SWBDAnalysis
import operator
class Model:

    def __init__(self, corpus, typeOfAnalysis, speakersInfos=None, monocorpusAnalysis= False, orderXaxis="no"):
        """

        :param corpus:
        :param speakersInfos:
        :param monocorpusAnalysis:
        :param orderXaxis: possible values {no,byX ,byY}
        """
        self.__corpora = corpus
        self.__associatedInputs = []
        self.__corpusToAnalyzeNames = "*"
        self.__monocorpusAnalysis = monocorpusAnalysis
        self.__xAxis = set()  # will contain the possible values of x
        self.__x = None  # will contain the values on x axis
        self.__y = None  # will contain the values on y axis
        self.__bottom = None  # will be used for the value of a vbar bottom (regarding the x axis)
        self.__q1 = None
        self.__q3 = None
        self.__AnalysisFct = None  # eg(number of lines)
        self.__color = None
        self.__discriminationCriterion = None  # eg age, sex
        self.__option1 = None  # an input that isn't used for the same thing
        self.__legend = None
        self.__speakersInfos = speakersInfos
        self.__orderXaxis = orderXaxis
        self.__typeOfAnalysis = typeOfAnalysis
        self.__tooltips = {}


    def getXAxis(self):
        return copy.copy(self.__xAxis)

    def getX(self):
        return copy.copy(self.__x)

    def getY(self):
        return copy.copy(self.__y)

    def getBottom(self):
        return copy.copy(self.__bottom)

    def getQ1(self):
        return copy.copy(self.__q1)

    def getQ3(self):
        return copy.copy(self.__q3)

    def setDiscriminationCriterion(self, discriminationCriterion):
        self.__discriminationCriterion = discriminationCriterion

    def analyseCorpus(self, corpus):
        """
        process a statistic analysis on the given corpus given the typeOfAnalysis (eg: nombre de mots)
        :param corpus: Corpus instance
        :return:
        """
        if not isinstance(self.__AnalysisFct, str):
            print("typeOfAnalysis must be a string")
            return -1
        if 'number of IPU by file' == self.__AnalysisFct:
            data = pd.Series(corpus.getNbOfLines(forEachFile=True))
        elif 'number of IPU' == self.__AnalysisFct:
            data = corpus.getNbOfLines()

        elif 'number of words by file' == self.__AnalysisFct:
            data = pd.Series(corpus.getNumberOfWords(forEachFile=True))

        elif 'time by file' == self.__AnalysisFct:
            data = pd.Series(corpus.getDuration(forEachFile=True))
            data /= 60

        elif 'words/IPU by file' == self.__AnalysisFct:
            data = pd.Series(corpus.getNumberOfWords(forEachFile=True))
            ipuParFichier = corpus.getNbOfLines(forEachFile=True)

            for i in range(0, len(data)):
                data[i] /= ipuParFichier[i]


        elif 'seconds/IPU by file' == self.__AnalysisFct:
            data = pd.Series(corpus.getDuration(forEachFile=True))
            nbOfLines = corpus.getNbOfLines(forEachFile=True)
            for i in range(0, len(data)):
                if nbOfLines[i] != 0:
                    data[i] /= nbOfLines[i]


        elif "words/seconds by file" == self.__AnalysisFct:
            data = corpus.getNumberOfWords(forEachFile=True)
            durationByFile = corpus.getDuration(forEachFile=True)
            for i in range(0, len(data)):
                if durationByFile[i] == 0:
                    data[i] = 0
                    continue
                data[i] = data[i] / durationByFile[i]

            data = pd.Series(data)

        elif "number of files" in self.__AnalysisFct:
            # number of files by files
            data = pd.Series([1] * corpus.getNbOfFiles())  # send back the number of file in each file stupid but it helps abstraction

        elif self.__AnalysisFct == "freqDist":
            data = corpus.distFrequency()

        elif self.__AnalysisFct == "time":
            data = corpus.getDuration()
            data /= 3600

        elif self.__AnalysisFct == "number of words by file":
            data = corpus.getNumberOfWords(forEachFile=True)
        elif self.__AnalysisFct == "number of words":
            data = corpus.getNumberOfWords()

        else:
            print("invalid analyze function " + str(self.__AnalysisFct))
            return
        return data

    def analyseMultipleCorpus(self):
        """
        analyse corpus in self.__corpusToAnalyzeNames or all of them if self.__corpusToAnalyzeNames is equal to "*"
        set the data that the analysis return in the object attributes
        :return:
        """
        if self.__AnalysisFct is None:  # it means that other input are changing before the input of analysis
            return
        for corpus in self.__corpora:
            if (corpus.getName() in self.__corpusToAnalyzeNames) or (self.__corpusToAnalyzeNames == "*"):
                self.__xAxis.add(corpus.getName())
                self.__x.append(corpus.getName())
                data = self.analyseCorpus(corpus)
                if isinstance(data, pd.Series):
                    self.__bottom.append(data.min())
                    self.__y.append(data.max())
                    self.__q1.append(data.quantile(0.25))
                    self.__q3.append(data.quantile(0.75))

                else:
                    self.__bottom.append(0)
                    self.__y.append(data)

        if self.__xAxis == set():
            print("no data available with this corpus name")

    def createDataSpeakerAnalysis(self, corpusName, speakers):
        """
        :param corpusName: str name of the corpus to analyse
        :param speakers: :param speakersId: {'1268': {'age': '29', 'geography': 'SOUTH MIDLAND', 'level_study': '2', 'sex': 'FEMALE'},'1269'...
        :return:
        """
        corpus = None
        # getting all the corpus that correspond to given corpus names
        for c in self.__corpora:
            if c.getName() == corpusName:
                corpus = c
                break

        if corpus == None:
            print("no corpus with name " + str(corpusName))
            return -1

        eachFilespeakerID = corpus.getSpeakerByFile()

        eachCorpusSpeakers = []  # [{'age': '29', 'geography': 'SOUTH MIDLAND', 'level_study': '2', 'sex': 'FEMALE'},{...]
        for speakerId in eachFilespeakerID:
            eachCorpusSpeakers.append(speakers[speakerId])

        # getting the data for each file (eg number of words by file)
        data = self.analyseCorpus(corpus)

        # checking if each speaker has the criterion we are looking for (eg: male, age)
        for speaker in eachCorpusSpeakers:
            if self.__discriminationCriterion not in speaker:
                print("unrecognized speaker discrimination" + str(self.__discriminationCriterion))
                return -1

        dataBySpeakerType = {} # at the end will look like {"male": 123, "female" : 456}
        for speakerNb in range(0, len(eachCorpusSpeakers)):
            speakerType = eachCorpusSpeakers[speakerNb][self.__discriminationCriterion]  # eg: male or female

            if speakerType in dataBySpeakerType:
                dataBySpeakerType[speakerType] += data[speakerNb]
            else:
                dataBySpeakerType[speakerType] = data[speakerNb]

        # checking if each type is a digit
        isDigitType = True
        for key in dataBySpeakerType.keys():
            if not key.isdigit():
                isDigitType = False
                break

        xAxis = set()
        y = []

        # if there's too many x axis values and we group values together
        # we group values eg: 1 2 3 4 -> 1_2 3_4
        if isDigitType and len(dataBySpeakerType.keys()) > 10:
            sortedData = sorted(dataBySpeakerType.items(), key=operator.itemgetter(0))

            arr = np.array_split(np.array(sortedData), 10)
            for element in arr:
                xAxis.add(str(element[0][0])+"_"+str(element[-1][0]))
                value = 0
                for tuple in element:

                    value += float(tuple[1])

                y.append(value)
            xData = list(xAxis)
        else:

            xData = [k for k in dataBySpeakerType.keys()]
            for element in xData:
                xAxis.add(element)
            for key in dataBySpeakerType:
                y.append(dataBySpeakerType[key])

        self.__xAxis = xAxis
        self.__y = y
        self.__x = xData

    # ---------------------------------------------------------------------------------

    def __call__(self, *args):
        """
        used to refresh the infos of the model
        :param args:
        :return:
        """
        self.__x = []
        self.__xAxis = set()
        self.__y = []
        self.__bottom = []
        self.__q1 = []
        self.__q3 = []
        self.refreshInputInfos()

        if self.__typeOfAnalysis == "speakers":
        #if self.__discriminationCriterion != None and self.__speakersInfos != None:
            for corpus in self.__corpora:
                if corpus.getName() in self.__corpusToAnalyzeNames:
                    if corpus.getName() in self.__speakersInfos:
                        self.createDataSpeakerAnalysis(corpus.getName(), self.__speakersInfos[corpus.getName()])
                        break
        elif self.__typeOfAnalysis == "mutipleCorpus":
        #elif self.__monocorpusAnalysis == False:
            self.analyseMultipleCorpus()

        elif self.__typeOfAnalysis == "freq":
        #else:  #it's a frequency distribution
            for corpus in self.__corpora:
                if (corpus.getName() in self.__corpusToAnalyzeNames):
                    data = self.analyseCorpus(corpus)

                    self.__x = list(data.keys())
                    self.__y = list(data.values())

        elif self.__typeOfAnalysis == "pca":

            for corpus in self.__corpora:

                if (corpus.getName() in self.__corpusToAnalyzeNames) or self.__corpusToAnalyzeNames == "*":
                    # getting the DATA
                    dataframe = None
                    speakersIDs = None
                    if isinstance(self.__option1, str):

                        if self.__option1.isdigit():
                            # speakersIDs is ordered in the dataframe way
                            dataframe, speakersIDs = SWBDAnalysis(corpus, self.__speakersInfos["SWBD"], numberOfWords=10
                                                     , clusterKMean=int(self.__option1))
                        else:
                            dataframe, speakersIDs = SWBDAnalysis(corpus, self.__speakersInfos["SWBD"], numberOfWords=10
                                                 , labelWanted=self.__option1)
                    else:
                        print("can't use self.__option1, must be a string not :" + str(type(self.__option1)))

                    # Proceeding to PCA
                    df, pcaObject = pca(dataframe)
                    self.__x = list(df["principal component 1"])
                    self.__y = list(df["principal component 2"])

                    # managing colors
                    labels = df["label"].unique()
                    availableColors = ["green", "blue", "black", "red", "yellow", "purple", "pink", "grey", "brown"]
                    if len(labels) > len(availableColors):
                        availableColors.extend("black" for i in range(100))

                    colorForLabel = dict(zip(labels, availableColors))
                    colors = []
                    for label in df["label"]:
                        colors.append(colorForLabel[label])

                    self.__color = colors

                    self.defXAxis()

                    # preparing the tooltips
                    self.__tooltips = {}

                    # initiliaze an array for each type of information eg(sex, age etc)
                    for key in self.__speakersInfos["SWBD"][speakersIDs[0]]:
                        self.__tooltips[key] = []

                    for sID in speakersIDs:
                        speakerData = self.__speakersInfos["SWBD"][sID]
                        for infoType in speakerData:
                            self.__tooltips[infoType].append(speakerData[infoType])
                    #     self.__tooltips["speakerId"].extend(self.__speakersInfos["SWBD"][sID])

                    # adding speaker IDs inside to the tooltips
                    self.__tooltips["speakerID"] = speakersIDs

                    # managing the legend

                    # legends = dataframe["label"].unique()
                    #labels = dataframe["label"]
                    # for word in legends:
                    #     self.__legend[word] = labels[labels == word].index[0]
                    self.__legend = df["label"]

                    continue  # for now pca analysis is only intended for one corpus



        else:
            print("unknown self.__typeOfAnalysis in Model.py")

        self.defXAxis()

    # ---------------------------------------------------------------------------------

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
                self.__AnalysisFct = input.getValue()
            elif dataType == "option1":
                self.__option1 = input.getValue()
            else:
                print("unrecognized data type" + input.getDataType())

    def setTypeOfAnalysis(self, typeOfAnalysis):
        self.__AnalysisFct = typeOfAnalysis



    def addAssociatedInput(self, input):
        """
        add an input to the model, link it to the model and refresh the model infos
        :param input: instance of Input
        :return:
        """
        self.__associatedInputs.append(input)
        input.observe(self)
        self.refreshInputInfos()

    def defXAxis(self):
        if self.__x is None:
            return
        if "no" == self.__orderXaxis:
            self.__xAxis = set(self.__x)
        elif "can't" == self.__orderXaxis:
            # will be done by bokeh automatically
            pass



        elif "byY" == self.__orderXaxis:  # order by increasing y
            xy = zip(self.__y, self.__x)

            xy = sorted(xy, key=lambda y: y[0])

            self.__xAxis = [i[1] for i in xy]
        elif "byX" == self.__orderXaxis:  # order by increasing x

            if self.__x[0].isdigit() or isinstance(self.__x[0], str):
                xy = zip(self.__y, self.__x)

                xy = sorted(xy, key=lambda y: y[1])

                self.__xAxis = [i[1] for i in xy]

            elif "_" in self.__x[0]:  # in case of a range (eg 1_3)
                temp = []
                for x in self.__x:
                    temp.extend(x.split('_')[0])

                xtemp = zip(self.__x, temp)

                xtemp = sorted(xtemp, key=lambda y: y[1])

                self.__xAxis = [i[1] for i in xtemp]
            else:
                print("can't order by x")

    def getColors(self):
        return copy.copy(self.__color)

    def getTooltips(self):
        return copy.copy(self.__tooltips)

    def getLegend(self):
        return copy.copy(self.__legend)


