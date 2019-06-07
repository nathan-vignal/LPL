from __future__ import print_function
from bokeh.io import output_notebook
from bokeh import server
from source.Simone.functions import download_data, visualize_timing
import os
from IPython.display import display
from source.pathManagment import getOriginePath, getPathToSerialized
from source.corpusRelated.CorpusReader import createCorpusFromDirectory
from source.corpusRelated.Speakers import getSpeakers
from source import RadarGraph
from source import RadarModel
import warnings
import time
import ipywidgets as widgets
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from source.Graph import Graph
from source import Cell
from source import Model
from source import Input
from bokeh.io import curdoc
import pickle

# !!!!!!!!!! import for notebook !!!!!!!!!!
from source.DimensionalityReduction import analysisInManyDimensions\
    , pca\
    , displayPlot\
    , SWBDAnalysis\
    , freqAnalysis
# !!!!!!!!!! import for notebook !!!!!!!!!!

warnings.filterwarnings("ignore")  # to avoid the displaying of a warning caused by the bokeh library...

output_notebook()

metaDataToLoad = ["sex", "age", "geography", "level_study"]

metaDataFiles = {"SWBD": os.path.join(getOriginePath(), "data", "metadata")}
conversationInfo = {}
speakers = {}
for corpusName in metaDataFiles:
    tempConversationInfo, tempspeakers = getSpeakers(metaDataFiles[corpusName], metaDataToLoad)
    conversationInfo[corpusName] = tempConversationInfo
    speakers[corpusName] = tempspeakers

f = open(os.path.join(getPathToSerialized(), "swbdSpeakers"), "wb")
pickle.dump(speakers, f)
f.close()


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

    model = Model.Model(arrayOfCorpus, "mutipleCorpus")
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


def analysisByConversation(corpusNames):
    corpora = choosingCorpora(corpusNames)
    cell = Cell.Cell()
    graph = Graph()
    # In this dictionnary you can link an analysis function with a keyword of your choice that will
    # be diplayed in a input
    analysisFunctions = {'number of IPU': 'number of IPU by file',
                         'number of words': 'number of words by file',
                         'time': 'time by file',
                         'words/IPU': 'words/IPU by file',
                         'seconds/ipu': 'seconds/IPU by file',
                         'words/seconds': 'words/seconds by file'}

    input = Input.Input("radio", "analysisFunction", graph, analysisFunctions
                        , "analysis functions"
                        )

    options = []
    for corpus in corpora:
        options.append(corpus.getName())
    inputCorpus = Input.Input("checkboxGroup", "corpusNames", graph, options, "Corpus")

    model = Model.Model(corpora, "mutipleCorpus")
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

    model = Model.Model(corpora, "speakers", speakers, orderXaxis="byX")
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
    model = Model.Model(corpora, "freq", monocorpusAnalysis=True, orderXaxis="byY")
    model.setTypeOfAnalysis("freqDist")
    model.addAssociatedInput(inputCorpus)
    graph.addGlyph("column", "VBar", model, option1=0.1, option2="#3AC0C3")
    cell.addGraph("unused", graph)
    cell.updateDisplay()


def contestPlot():

    swbd = choosingCorpora("swbd")  # this function focuses on switchboard
    cell = Cell.Cell()
    graph = Graph(tools="pan,wheel_zoom,box_zoom,reset,hover", iscontinuous=True)

    groupOptions = {
        "level of study": "level_study",
        "age": "age",
        "origin": "geography",
        "sex": "sex",
        "3": "3",
        "4": "4",
        "5": "5",
    }

    inputGroups = Input.Input("radio", "option1", graph, groupOptions, "goups")
    cell.addInput(" ", inputGroups)

    model = Model.Model(swbd, "pca", speakers, orderXaxis="can't")
    model.setTypeOfAnalysis("sex")
    pos = ColumnDataSource(data=dict(x=[], y=[]))
    graph.addGlyph("scatterDots", "scatter", model, option1=10, option3=pos)
    cell.addGraph("graph1", graph)
    model.addAssociatedInput(inputGroups)
    model()

    button = widgets.Button(description="Search")
    input = widgets.IntText(description="conversation id", continuous_update=False)
    display(button)
    display(input)

    def on_button_clicked(b):
        # if input.value in
        leftSide(input.value)

    button.on_click(on_button_clicked)

    cell.updateDisplay()
    # leftSide(2010)  # temporary for dev purpose # debug
    # time.sleep(1)  # debug
    # leftSide(2001)  # temporary for dev purpose# debug

leftSideFigure = None
ax = None
def leftSide(id_conv):
    global leftSideFigure
    global ax
    # Download RAW Data ( is a dataframe that contain all the token for each conversation of the corpus)
    N_directory = 20
    RAW_data = download_data(N_directory, 'X')
    N_directory_save = 20
    N_directory_download = 20
    download_silence = 1

    # Download Processed Data (basically contain a new segmentation of the turns)
    N_directory = 10
    N_directory_download = 10
    download_label = 1
    min_time_silence = 1.5

    # download conversation labeled
    min_time_silence_ms = min_time_silence * 1000
    name_download = 'conversation_label_silence' + str(int(min_time_silence_ms)) + 'ms'
    conversation_tot_new = download_data(N_directory_download, name_download)

    x = 0  # start time point
    delta = 0  # interval length( if <= 0 it takes by default the end of the conversation)

    # chose the type of token we want to visualize in the conversation. It will display anyway in Orange colour
    # all the tokens not specified n the list
    no_content_token_list = ['[silence]', '[noise]', '[vocalized-noise]', '[laughter]', 'yeah', 'right', 'um-hum',
                             'uh-huh', 'right', 'mh', 'okay']  # list of no-informative words
    # Assign at each token of the list "no_content_token_list" a colour
    list_color = ["palegreen", "gray", "gray", "violet", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue",
                  "blue"]
    leftSideFigure, ax = visualize_timing(id_conv, conversation_tot_new, no_content_token_list, x, delta, list_color
                                      , leftSideFigure, ax)  # RAW DATA
    leftSideFigure.canvas.draw()
    # leftSideFigure.canvas.draw()
    # plt.show()











