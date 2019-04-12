# -*- coding: iso-8859-1 -*-
from __future__ import print_function
from IPython.display import display
from bokeh.models import ColumnDataSource
from ipywidgets import interact, interactive, fixed, interact_manual
from bokeh.models.glyphs import VBar
import ipywidgets as widgets
from bokeh.plotting import figure, output_file, gridplot
from bokeh.io import output_notebook, show, push_notebook
import pandas as pd
from os import listdir
import math
import Corpus
import File
output_notebook()


boxplot_data_source = 0
boxplotHandle = 0
segments_data_source = 0
rect_data_source = 0

sourcedirectory = "C:/Users/vignal/Documents/corpus/"
corpuses = []
# search source directory for corpus and fill corpus object with files inside array corpuses
for directoryName in listdir(sourcedirectory):
    path = sourcedirectory + directoryName
    newCorpus = Corpus.Corpus(directoryName, sourcedirectory + directoryName, directoryName)

    files = []
    if directoryName == "Fisher":
        path = sourcedirectory + directoryName + "/Fisher1/data/bbn_orig/"
        for directory in listdir(path):
            for file in listdir(path + directory + "/auto-segmented"):
                if "TRN" in file:
                    print(file)
        break

    for filename in listdir(path):
        # the directory for switchboard has a specific architecture
        if directoryName == 'SWBD' :
            for swbdDirectory in listdir(path+'/'+filename):
                for file in listdir(sourcedirectory + directoryName+'/'+filename+'/'+swbdDirectory):
                    if "trans" in file:
                        currentFile = File.File(sourcedirectory + directoryName+'/'+filename+'/'+swbdDirectory+'/'+file
                                            ,newCorpus.delimiter)
                        files.append(currentFile)
            break

        currentFile = File.File(sourcedirectory+directoryName+"/"+filename, newCorpus.delimiter)
        files.append(currentFile)

    newCorpus.addElements(files)
    corpuses.append(newCorpus)

# radioButton to choose how to analyze the data
fctAnalyse = widgets.RadioButtons(
    options=['nombre d \'IPU par fichier',
             'nombre de mots par fichier',
             'temps par fichier',
             'mots/ipu par fichier',
             'secondes/ipu par fichier',
             'mots/secondes'
             ],
     value='nombre d \'IPU par fichier',
    description='options d\'analyse',
    disabled=False
)
display(fctAnalyse)

def createBoxPlot(corpusToAnalyze):
    """
    create or update a boxplot depending on what are the corpuses to analyze
    and on the status of the radio buttons fctAnalyze
    :param corpusToAnalyze:
    :return:
    """
    global boxplot_data_source
    global fctAnalyse
    global boxplotHandle
    global segments_data_source
    global rect_data_source
    # data regarding corpuses boxplot style
    xAxisData = []
    mins = []
    maxs = []
    q1 = []
    q3 = []
    if  boxplot_data_source == 0:
        boxplot_data_source = ColumnDataSource(data=dict())
    title = ""
    for corpus in corpuses:
        if corpus.getName() in corpusToAnalyze:
            if 'nombre d \'IPU' in fctAnalyse.value:
                data = pd.Series(corpus.getNbOfLinesByFile())
            elif 'nombre de mots' in fctAnalyse.value:
                data = pd.Series(corpus.getNumberOfWordsByFile())
            elif "temps par fichier" in fctAnalyse.value:
                data = pd.Series(corpus.getDurationByFile())
                data /= 60
            elif "mots/ipu" in fctAnalyse.value:
                data = pd.Series(corpus.getNumberOfWordsByFile())
                ipuParFichier = corpus.getNbOfLinesByFile()
                for i in range(0,len(data)):
                    data[i] /= ipuParFichier[i]
            elif "secondes/ipu" in fctAnalyse.value:
                data = pd.Series(corpus.getDurationByFile())
                nbOfLines = corpus.getNbOfLinesByFile()
                for i in range(0, len(data)):
                    data[i] /= nbOfLines[i]
            elif "mots/secondes" in fctAnalyse.value:
                data = corpus.getNumberOfWordsByFile()
                durationByFile = corpus.getDurationByFile()
                for i in range(0, len(data)):
                    data[i] = data[i] / durationByFile[i]
                data = pd.Series(data)
            else:
                print("invalid analyze function ")
                data = []  # prevent crash

            xAxisData.append(corpus.getName())
            mins.append(data.min())
            maxs.append(data.max())
            q1.append(data.quantile(0.25))
            q3.append(data.quantile(0.75))
        if segments_data_source == 0:
             segments_data_source = ColumnDataSource(data=dict(x=xAxisData, top=maxs, bottom=mins))
             rect_data_source = ColumnDataSource(data=dict(x=xAxisData, top=q3, bottom=q1))
        else:
            segments_data_source.data = {'x':xAxisData, 'top':maxs, 'bottom':mins}
            rect_data_source.data = {'x':xAxisData, 'top':q3, 'bottom':q1}

    #boxplot_data_source.data = {'x_range':xAxisData, 'title':title}
    if boxplotHandle == 0: #if it's the first time
        boxplot = figure(x_range=xAxisData, title="title", tools="")
        segments = VBar(x="x", top="top", bottom="bottom", width=0.01, fill_color="black")  # segments
        rectangles = VBar(x="x", top="top", bottom="bottom", width=0.1, fill_color="red")  # rectangles
        boxplot.add_glyph(segments_data_source, segments)
        boxplot.add_glyph(rect_data_source, rectangles)#boxplot_data_source,
        boxplotHandle = show(boxplot, notebook_handle=True)
    else:
        push_notebook(handle=boxplotHandle)



corpusInputs = []
for corpus in corpuses:
    temp = widgets.Checkbox(
    value=True,
    description=corpus.getName()
    )
    corpusInputs.append(temp)



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
            if corpusCheckbox.description in corpusToAnalyze: corpusToAnalyze.remove(
                corpusCheckbox.description.encode("utf-8"))
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
    display(input)

fctAnalyse.observe(refreshBoxplot)

# display
corpusToDisplay = []
for corpus in corpuses:
    corpusToDisplay.append(corpus.getName())


createBoxPlot(corpusToDisplay)





