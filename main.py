# -*- coding: iso-8859-1 -*-
from __future__ import print_function
from IPython.display import display
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
import ipywidgets as widgets
from bokeh.plotting import figure, output_file, gridplot
from bokeh.io import output_notebook, show, push_notebook
import pandas as pd
import numpy as np
from os import listdir
from CorpusReader import createCorpusFromDirectory
from Speakers import getSwbdSpeakers
from AnalyseStat import analyseCorpus
import Corpus
import File
import Fisher
import FileWithSpeaker
import warnings
warnings.filterwarnings("ignore")  # to avoid the displaying of a warning caused by the bokeh library...

output_notebook()

# global variable for first plot
boxplot_data_source = None
boxplotHandle = None
segments_data_source = None
rect_data_source = None
# end global variable for first plot

# global variable for second plot
discr_data_source = None
discrPlotHandler = None
discrPlot = None
# end global variable for second plot

# global variable for third plot
dataBySpeaker_data_source = None
# end global variable for third plot



metaDataToLoad = ["sex", "age", "geography", "level_study"]
conversationInfo, speakers = getSwbdSpeakers("C:/Users/vignal/Documents/metadata/", metaDataToLoad)


def initCorpus(sourceDirectory):
    global conversationInfo
    arrayOfCorpus = []
    # search source directory for corpus and fill corpus object with files inside array corpuses
    for directoryName in listdir(sourceDirectory):
        newCorpus = createCorpusFromDirectory(directoryName, sourceDirectory +'/' + directoryName, conversationInfo)
        #print(newCorpus.getName())
        #print(newCorpus.getNbOfLinesByFile())
        arrayOfCorpus.append(newCorpus)
    return arrayOfCorpus


arrayOfCorpus = initCorpus("C:/Users/vignal/Documents/corpus/")


def createFirstCell():
    # radioButton to choose how to analyze the data
    fctAnalyse = widgets.RadioButtons(
        options=['nombre d\'IPU par fichier',
                 'nombre de mots par fichier',
                 'temps par fichier',
                 'mots/ipu par fichier',
                 'secondes/ipu par fichier',
                 'mots/secondes'
                 ],
        value='nombre d\'IPU par fichier',
        description='options d\'analyse',
        disabled=False
    )

    def createBoxPlot(corpusToAnalyze):
        """
        create or update a boxplot depending on what are the corpuses to analyze
        and on the status of the radio buttons fctAnalyze
        :param corpusToAnalyze:
        :return:
        """
        global boxplot_data_source
        global boxplotHandle
        global segments_data_source
        global rect_data_source
        # data regarding corpuses boxplot style
        xAxisData = []
        mins = []
        maxs = []
        q1 = []
        q3 = []
        if boxplot_data_source == None:
            boxplot_data_source = ColumnDataSource(data=dict())
        for corpus in arrayOfCorpus:
            if corpus.getName() in corpusToAnalyze:
                data = analyseCorpus(fctAnalyse.value, corpus)

                xAxisData.append(corpus.getName())
                mins.append(data.min())
                maxs.append(data.max())
                q1.append(data.quantile(0.25))
                q3.append(data.quantile(0.75))
            if segments_data_source == None:
                segments_data_source = ColumnDataSource(data=dict(x=xAxisData, top=maxs, bottom=mins))
                rect_data_source = ColumnDataSource(data=dict(x=xAxisData, top=q3, bottom=q1))
            else:
                segments_data_source.data = {'x': xAxisData, 'top': maxs, 'bottom': mins}
                rect_data_source.data = {'x': xAxisData, 'top': q3, 'bottom': q1}

        # boxplot_data_source.data = {'x_range':xAxisData, 'title':title}
        if boxplotHandle == None:  # if it's the first time
            boxplot = figure(x_range=xAxisData, title="title", tools="")
            segments = VBar(x="x", top="top", bottom="bottom", width=0.01, fill_color="black")  # segments
            rectangles = VBar(x="x", top="top", bottom="bottom", width=0.1, fill_color="red")  # rectangles
            boxplot.add_glyph(segments_data_source, segments)
            boxplot.add_glyph(rect_data_source, rectangles)  # boxplot_data_source,
            boxplotHandle = show(boxplot, notebook_handle=True)
        else:
            push_notebook(handle=boxplotHandle)

    corpusInputs = []
    verticalBoxCorpus = widgets.VBox()
    for corpus in arrayOfCorpus:
        temp = widgets.Checkbox(
            value=True,
            description=corpus.getName()
        )
        corpusInputs.append(temp)
    verticalBoxCorpus.children = corpusInputs

    def processCorpusToAnalyze():
        """
        create an array of corpus to analyze from the values of the corpusCheckboxes
        :return:
        """
        corpusToAnalyze = []
        for corpusCheckbox in corpusInputs:
            if corpusCheckbox.value:
                corpusToAnalyze.append(corpusCheckbox.description.encode("utf-8"))
            else:
                if corpusCheckbox.description in corpusToAnalyze:
                    corpusToAnalyze.remove(corpusCheckbox.description.encode("utf-8"))
        createBoxPlot(corpusToAnalyze)

    def refreshBoxplot(b):
        """
        call processCorpusToAnalyze just on time went the observer of an item is triggered
        :param b:
        :return:
        """
        if type(b.new) == type(True) or type(b.new) == type(""):  # the observe function trigger multiple
            # times on each update this condition makee sure it
            # only does so once
            processCorpusToAnalyze()

    for input in corpusInputs:
        input.observe(refreshBoxplot)


    fctAnalyse.observe(refreshBoxplot)

    # display
    corpusToDisplay = []
    for corpus in arrayOfCorpus:
        corpusToDisplay.append(corpus.getName())

    hBox = widgets.HBox([fctAnalyse, verticalBoxCorpus])
    createBoxPlot(corpusToDisplay)
    display(hBox)

# end creatFirstCell



def createSecondCell():
    """
    analysis menu regarding switchboard
    :return:
    """
    global metaDataToLoad
    swbd = 0  # will contain the corpus switchboard
    for corpus in arrayOfCorpus:
        if corpus.getName() == "SWBD":
            swbd = corpus
            break
    if swbd == 0:
        print("can't find SWBD in the corpus")
        return -1

    analysisOptions = ['nombre d\'IPU par fichier',
                 'nombre de mots par fichier',
                 'temps par fichier',
                'nombre de fichier'
                 ]
    fctAnalyseSWBD = widgets.RadioButtons(
        options=analysisOptions,
        value=analysisOptions[0],
        description='options d\'analyse',
        disabled=False
    )
    speakerDiscrimination = widgets.RadioButtons(
        options=metaDataToLoad,
        value=metaDataToLoad[0],
        description='discrimination',
        disabled=False
    )

    def createOrRefreshDiscrPlot():
        global discr_data_source
        global discrPlotHandler
        global discrPlot
        eachFilespeakerID = swbd.getSpeakerByFile()
        eachFilespeaker = []
        for id in eachFilespeakerID:
            eachFilespeaker.append(speakers[id])

        data = analyseCorpus(fctAnalyseSWBD.value,swbd)
        dataBySpeakerType = {}
        discriminationCritirion = speakerDiscrimination.value
        for speakerData in eachFilespeaker:
            if discriminationCritirion not in speakerData:
                print("unrecognized speaker discrimination" + str(discriminationCritirion))
                return -1

        for i in range(0, len(data)):
            speakerType = eachFilespeaker[i][discriminationCritirion]
            if speakerType in dataBySpeakerType:
                dataBySpeakerType[speakerType] += data[i]
            else:
                dataBySpeakerType[speakerType] = data[i]
        # check if all the keys are in the same type
        # types = [type(k) for k in dataBySpeakerType.keys()]
        # for i in range(0,len(types)-1):
        #     if types[i] != types[i+1]:
        #         print("all keys are not in the same type (createOrRefreshDiscrPlot)" + str(types[i]) + str(types[i+1]))
        #print(dataBySpeakerType.keys()[0])
        xData = None
        xAxis = None
        y = None
        # if there's too many x axis value and we can group can group them, we group values together
        # eg 1 2 3 4 -> 1_2 3_4
        if dataBySpeakerType.keys()[0].isdigit() and len(dataBySpeakerType.keys()) > 10:

            for key in dataBySpeakerType.keys():
                xData.append(key)
                y = [dataBySpeakerType.keys()[key]]
            # if there is too many categories we create groups
            xAxis = np.sort(np.asarray(xData))

            np.split(xAxis, 10)


        else :
            xData = [k for k in dataBySpeakerType.keys()]
            xAxis = xData
            y = []
            for key in dataBySpeakerType:
                y.append(dataBySpeakerType[key])
            # sorting the bars means sorting the range factors
            xAxis = sorted(xData, key=lambda x: y[xData.index(x)])  # xAxis contains the values that will serve
            # as the x axis values eg (male, Female)


        if discr_data_source == None:
            discr_data_source = ColumnDataSource(data=dict(x=xData, top=y))
            discrPlot = figure(x_range=xAxis, tools="")
            bars = VBar(x="x", top="top", width=0.1, fill_color="black")  # segments
            discrPlot.add_glyph(discr_data_source, bars)
            discrPlotHandler = show(discrPlot, notebook_handle=True)
        else:
            discrPlot.x_range.factors = xAxis
            discr_data_source.data = {"x": xData, "top": y}
            push_notebook(handle=discrPlotHandler)



    def discrMenuInput(widget):
        if type(widget.new) == type(""):
            createOrRefreshDiscrPlot()

    speakerDiscrimination.observe(discrMenuInput)
    fctAnalyseSWBD.observe(discrMenuInput)

    hBoxDiscrimination = widgets.HBox([fctAnalyseSWBD, speakerDiscrimination])
    display(hBoxDiscrimination)
    createOrRefreshDiscrPlot()
# end createSecondCell


def createThirdCell():
    global conversationInfo
    global speakers
    global dataBySpeaker_data_source
    xAxisData = []
    corpusWithSpeakerData = []  # will contain the corpus that have metadata about speakers
    for corpus in arrayOfCorpus:
        if corpus.getName() == "SWBD": # for now is the only corpus that contain metadataa about the speakers
            corpusWithSpeakerData.append(corpus)
            xAxisData.append(corpus.getName())
            break
    if corpusWithSpeakerData == []:
        print("Aucun copus ne contient de données sur le locuteur")
        return -1

    f = figure(x_range=xAxisData)
    y = []
    dataBySpeaker = []
    for corpus in corpusWithSpeakerData:
        dataBySpeaker.append(zip(corpus.getDurationByFile(), corpus.getSpeakerByFile()))
    # for item in dataBySpeaker:
    #     for i in item:
    #         print(i)
    speakerData = {}
    #for i in range()



    # if dataBySpeaker_data_source == None:
    #     dataBySpeaker_data_source = ColumnDataSource(data=dict(x_range = y=y))
    # vbar = VBar(x="x", top="top", width=0.1, fill_color="black")  # segments
    # f.add_glyph()

# end createThirdCell
# createThirdCell()
# createSecondCell()











