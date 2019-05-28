from __future__ import print_function
from bokeh.io import output_notebook
import os
from source.pathManagment import getOriginePath, getPathToSerialized
from source.corpusRelated.CorpusReader import createCorpusFromDirectory
from source.corpusRelated.Speakers import getSpeakers
from source import RadarGraph
from source import RadarModel
import warnings
from source.Graph import Graph
from source import Cell
from source import Model
from source import Input
import pickle

# !!!!!!!!!! import for notebook !!!!!!!!!!
from source.DimensionalityReduction import analysisInManyDimensions\
    , pca\
    , displayPlot\
    , SWBDAnalysisSpeakers\
    , freqAnalysis
# !!!!!!!!!! import for notebook !!!!!!!!!!

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

metaDataFiles = {"SWBD": os.path.join(getOriginePath(), "data", "metadata")}
conversationInfo = {}
speakers = {}
for corpusName in metaDataFiles:
    tempConversationInfo, tempspeakers = getSpeakers(metaDataFiles[corpusName], metaDataToLoad)
    conversationInfo[corpusName] = tempConversationInfo
    speakers[corpusName] = tempspeakers


def initCorpus():
    global conversationInfo
    arrayOfCorpus = []
    sourceDirectory = os.path.join(getOriginePath(), "data", "corpus")
    # search source directory for corpus and fill corpus object with files inside array corpuses
    for directoryName in os.listdir(sourceDirectory):
        newCorpus = createCorpusFromDirectory(directoryName, os.path.join(sourceDirectory, directoryName), conversationInfo)

        arrayOfCorpus.append(newCorpus)
    return arrayOfCorpus

# --------------------------------------------------------------------------------------------------------


arrayOfCorpus = initCorpus()

f = open(os.path.join(getPathToSerialized(), "arrayOfCorpus"), "wb")
pickle.dump(arrayOfCorpus, f)
f.close()

# f = open(os.path.join(getPathToSerialized(), "arrayOfCorpus"), "rb")
#
#
# arrayOfCorpus = pickle.load(f)
# f.close()


message = "available corpora : "
for corpus in arrayOfCorpus:
    message += "\n  - " + corpus.getName()
print(message)


# --------------------------------------------------------------------------------------------------------

def choosingCorpora(corpusNames):
    """

    :param corporaNames: should look like this "SWBD, cid, fisher"
    :return:
    """
    interestingCorpus = []
    if corpusNames == "all":
        interestingCorpus.extend(arrayOfCorpus)
    else:
        corporaNames = corpusNames.replace(" ", "").lower().split(',')

        for name in corporaNames:  # for each given names
            for corpus in arrayOfCorpus:  # for each corpus we have
                if name == corpus.getName().lower():
                    interestingCorpus.append(corpus)
                    break

    return interestingCorpus


# --------------------------------------------------------------------------------------------------------

def globalView(corpusNames):
    corpora = choosingCorpora(corpusNames)
    cell = Cell.Cell()

    model = Model.Model(arrayOfCorpus)
    graph = Graph()
    graph.addGlyph("column", "VBar", model, option1=0.2, option2="#3AC0C3")

    options = []
    for corpus in corpora:
        options.append(corpus.getName())

    inputCorpus = Input.Input("checkboxGroup", "corpusNames", graph, options, "Corpus")
    model.addAssociatedInput(inputCorpus)
    cell.addInput("corpus", inputCorpus)

    strToAnalysisFct = {"time": "time"
        , "number of words": "number of words"}

    input = Input.Input("radio", "analysisFunction", graph, strToAnalysisFct
                        , "analysis functions")

    model.addAssociatedInput(input)
    cell.addInput("analyse", input)
    cell.addGraph("unused", graph)
    cell.updateDisplay()


def AnalysisByFiles(corpusNames):
    corpora = choosingCorpora(corpusNames)
    cell = Cell.Cell()
    graph = Graph()
    # In this dictionnary you can link an analysis function with a keyword of your choice that will
    # be diplayed in a input
    analysisFunctions = {'number of IPU by speaker in conversation': 'number of IPU by file',
                         'number of words by speaker in conversation': 'number of words by file',
                         'time by speaker in conversation': 'time by file',
                         'words/IPU by speaker in conversation': 'words/IPU by file',
                         'seconds / ipu by speaker in conversation': 'seconds/IPU by file',
                         'words/seconds by speaker in conversation': 'words/seconds by file'}

    input = Input.Input("radio", "analysisFunction", graph, analysisFunctions
                        , "analysis functions"
                        )

    options = []
    for corpus in corpora:
        options.append(corpus.getName())
    inputCorpus = Input.Input("checkboxGroup", "corpusNames", graph, options, "Corpus")

    model = Model.Model(corpora)
    model.addAssociatedInput(input)
    model.addAssociatedInput(inputCorpus)
    cell.addInput("analyse", input)
    cell.addInput("corpus", inputCorpus)
    graph.addGlyph("segment", "VBarQuartile", model, option1=0.01, option2="#000000")
    graph.addGlyph("barres", "VBarQuartile", model, option1=0.2, option2="#3AC0C3")
    cell.addGraph("unused", graph)
    cell.updateDisplay()

# --------------------------------------------------------------------------------------------------------

def speakerAnalysis(corpusNames):
    """
    analysis menu regarding corpus with speakers
    :return:
    """
    corpora = choosingCorpora(corpusNames)
    cell = Cell.Cell()
    graph = Graph(tools="wheel_zoom")

    # In this dictionnary you can link an analysis function with a keyword of your choice that will
    # be diplayed in a input
    analysisFunctions = {
        'number of IPU': 'number of IPU by file'
        , 'number of words': 'number of words by file'
        , 'time': 'time by file'
        , 'number of conversations': 'number of files'
    }

    inputAnalyse = Input.Input("radio", "analysisFunction", graph, analysisFunctions
                               , "analysis functions"
                               )

    optionsDiscr = ["sex", "age", "geography", "level_study"]
    inputDiscr = Input.Input("radio", "discrimination", graph, optionsDiscr, "Discrimination")

    optionsCorpus = []
    for corpus in metaDataFiles:
        optionsCorpus.append(corpus)
    inputCorpus = Input.Input("radio", "corpusNames", graph, optionsCorpus, "Corpus")

    model = Model.Model(corpora, speakers, orderXaxis="byX")
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


def mutliCriterionAnalysis(corpusNames):
    corpora = choosingCorpora(corpusNames)

    cell = Cell.Cell()

    optionsCorpus = []
    for corpus in corpora:
        optionsCorpus.append(corpus.getName())
    graphRadar = RadarGraph.RadarGraph()
    inputCorpus = Input.Input("checkboxGroup", "corpusNames", graphRadar, optionsCorpus, "Corpus")
    cell.addInput("inputCorpus", inputCorpus)
    RadarModel.RadarModel(corpora, inputCorpus, graphRadar)
    cell.addGraph("unused", graphRadar)
    cell.updateDisplay()


def wordDistribution(corpusNames):
    corpora = choosingCorpora(corpusNames)
    cell = Cell.Cell()

    # testCorpus = [arrayOfCorpus[0],arrayOfCorpus[1]]
    # testCorpus.append(arrayOfCorpus[1])

    graph = Graph(tools="pan,wheel_zoom,box_zoom,reset,hover", y_axis_type="log")

    optionsCorpus = []
    for corpus in corpora:
        optionsCorpus.append(corpus.getName())

    inputCorpus = Input.Input("radio", "corpusNames", graph, optionsCorpus, "Corpus")
    cell.addInput(" ", inputCorpus)
    model = Model.Model(corpora, monocorpusAnalysis=True, orderXaxis="byY")
    model.setTypeOfAnalysis("freqDist")
    model.addAssociatedInput(inputCorpus)
    graph.addGlyph("column", "VBar", model, option1=0.1, option2="#3AC0C3")
    cell.addGraph("unused", graph)
    cell.updateDisplay()



#
# df = SWBDAnalysisSpeakers(arrayOfCorpus[4], speakers["SWBD"], "level_study", isFreqAnalysis=True)
# dataframe, pcaObject = pca(df)
# displayPlot(dataframe, groupByLabel=True)




















