from __future__ import print_function
from bokeh.io import output_notebook
from os import listdir
from corpusRelated.CorpusReader import createCorpusFromDirectory
from corpusRelated.Speakers import getSpeakers
from DimensionalityReduction import analysisInManyDimensions, pca, displayPlot
import RadarGraph
import RadarModel
import warnings
from Graph import Graph
import Cell
import Model
import Input
warnings.filterwarnings("ignore")  # to avoid the displaying of a warning caused by the bokeh library...

output_notebook()

# global variable for first plot
boxplotGraph = None
# end global variable for first plot

# global variable for second plot
discrGraph = {}
# end global variable for second plot

# global variable for third plot
dataBySpeaker_data_source = None
# end global variable for third plot


metaDataToLoad = ["sex", "age", "geography", "level_study"]
metaDataFiles = {"SWBD": "./data/metadata/"}
conversationInfo = {}
speakers = {}
for metadata in metaDataFiles:
    tempConversationInfo, tempspeakers = getSpeakers(metaDataFiles[metadata], metaDataToLoad)
    conversationInfo[metadata] = tempConversationInfo
    speakers[metadata] = tempspeakers


def initCorpus():
    global conversationInfo
    arrayOfCorpus = []
    sourceDirectory = "./data/corpus/"
    # search source directory for corpus and fill corpus object with files inside array corpuses
    for directoryName in listdir(sourceDirectory):
        newCorpus = createCorpusFromDirectory(directoryName, sourceDirectory + '/' + directoryName, conversationInfo)

        arrayOfCorpus.append(newCorpus)
    return arrayOfCorpus

# --------------------------------------------------------------------------------------------------------


arrayOfCorpus = initCorpus()
# to test arrayOfCorpus = [arrayOfCorpus[0], arrayOfCorpus[1]]


# --------------------------------------------------------------------------------------------------------

def globalView():

    cell = Cell.Cell()

    model = Model.Model(arrayOfCorpus)
    graph = Graph()
    graph.addGlyph("column", "VBar", model, option1=0.2, option2="#3AC0C3")

    options = []
    for corpus in arrayOfCorpus:
        options.append(corpus.getName())
    inputCorpus = Input.Input("checkboxGroup", "corpusNames", graph, options, "Corpus")
    model.addAssociatedInput(inputCorpus)
    cell.addInput("corpus", inputCorpus)

    options = ["time",
               "number of words"
               ]

    strToAnalysisFct = {"time": "time"
        , "number of words": "number of words"}

    input = Input.Input("radio", "analysisFunction", graph, options, "analysis functions"
                        ,strToAnalysisFct=strToAnalysisFct)

    model.addAssociatedInput(input)
    cell.addInput("analyse", input)
    cell.addGraph("unused", graph)
    cell.updateDisplay()


def AnalysisByFiles():
    # radioButton to choose how to analyze the data
    # global arrayOfCorpus    ##################################### test
    # arrayOfCorpus = [arrayOfCorpus[0]] ##################################### test
    cell = Cell.Cell()
    graph = Graph()
    options = ['number of IPU by file',
               'number of words by file',
               'time by file',
               'words/IPU by file',
               'seconds/IPU by file',
               'words/seconds by file'
               ]
    strToAnalysisFct = {'number of IPU by file' : 'number of IPU by file',
               'number of words by file' : 'number of words by file',
               'time by file' : 'time by file',
               'words/IPU by file' : 'words/IPU by file',
               'seconds/IPU by file' : 'seconds/IPU by file',
               'words/seconds by file' : 'words/seconds'}

    input = Input.Input("radio", "analysisFunction", graph, options, "analysis functions",
                        strToAnalysisFct=strToAnalysisFct)

    options = []
    for corpus in arrayOfCorpus:
        options.append(corpus.getName())
    inputCorpus = Input.Input("checkboxGroup", "corpusNames", graph, options, "Corpus")

    model = Model.Model(arrayOfCorpus)
    model.addAssociatedInput(input)
    model.addAssociatedInput(inputCorpus)
    cell.addInput("analyse", input)
    cell.addInput("corpus", inputCorpus)
    graph.addGlyph("segment", "VBarQuartile", model, option1=0.01, option2="#000000")
    graph.addGlyph("barres", "VBarQuartile", model, option1=0.2, option2="#3AC0C3")
    cell.addGraph("unused", graph)
    cell.updateDisplay()

# --------------------------------------------------------------------------------------------------------

def speakerAnalysis():
    """
    analysis menu regarding corpus with speakers
    :return:
    """
    cell = Cell.Cell()
    graph = Graph(tools="wheel_zoom")

    optionsAnalyse = ['number of IPU by file', 'number of words by file', 'time by file', 'number of files']
    inputAnalyse = Input.Input("radio", "analysisFunction", graph, optionsAnalyse, "analysis functions")

    optionsDiscr = ["sex", "age", "geography", "level_study"]
    inputDiscr = Input.Input("radio", "discrimination", graph, optionsDiscr, "Discrimination")

    optionsCorpus = []
    for corpus in metaDataFiles:
        optionsCorpus.append(corpus)
    inputCorpus = Input.Input("radio", "corpusNames", graph, optionsCorpus, "Corpus")

    model = Model.Model(arrayOfCorpus, speakers, orderXaxis="byX")
    model.addAssociatedInput(inputAnalyse)
    model.addAssociatedInput(inputDiscr)
    model.addAssociatedInput(inputCorpus)
    graph.addGlyph("column", "VBar", model, option1=0.2, option2="#3AC0C3")
    cell.addInput("analyse", inputAnalyse)
    cell.addInput("discrimination", inputDiscr)
    cell.addInput("corpus", inputCorpus)
    cell.addGraph("unused", graph)
    cell.updateDisplay()

# end createSecondCell


def mutliCriterionAnalysis():
    global arrayOfCorpus
    #  array with not every corpus to test code
    test = []
    test.append(arrayOfCorpus[0])
    test.append(arrayOfCorpus[1])
    # test.append(arrayOfCorpus[4])
    arrayOfCorpus = test

    cell = Cell.Cell()

    optionsCorpus = []
    for corpus in arrayOfCorpus:
        optionsCorpus.append(corpus.getName())
    graphRadar = RadarGraph.RadarGraph()
    inputCorpus = Input.Input("checkboxGroup", "corpusNames", graphRadar, optionsCorpus, "Corpus")
    cell.addInput("inputCorpus", inputCorpus)
    RadarModel.RadarModel(arrayOfCorpus, inputCorpus, graphRadar)
    cell.addGraph("unused", graphRadar)
    cell.updateDisplay()



def wordDistribution():
    cell = Cell.Cell()

    # testCorpus = [arrayOfCorpus[0],arrayOfCorpus[1]]
    # testCorpus.append(arrayOfCorpus[1])

    graph = Graph(tools="pan,wheel_zoom,box_zoom,reset,hover", y_axis_type="log")

    optionsCorpus = []
    for corpus in arrayOfCorpus:
        optionsCorpus.append(corpus.getName())

    inputCorpus = Input.Input("radio", "corpusNames", graph, optionsCorpus, "Corpus")
    cell.addInput(" ", inputCorpus)
    model = Model.Model(arrayOfCorpus, monocorpusAnalysis=True, orderXaxis="byY")
    model.setTypeOfAnalysis("freqDist")
    model.addAssociatedInput(inputCorpus)
    graph.addGlyph("column", "VBar", model, option1=0.1, option2="#3AC0C3")
    cell.addGraph("unused", graph)
    cell.updateDisplay()




print("end main.py")



















