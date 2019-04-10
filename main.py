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
previousSegment = 0
previousrectangles = 0
output_notebook()
boxplotHandle = 0
boxplot = 0
data_source = 0
rect_data_source = 0

sourcedirectory = "C:/Users/vignal/Documents/corpus/"
colormap = {'CID': 'red', 'DVD0': 'green', 'MTX': 'blue'}
corpuses = []

for directoryName in listdir(sourcedirectory):
    newCorpus = Corpus.Corpus(directoryName, sourcedirectory + directoryName, directoryName)
    currentDelimiter = newCorpus.delimiter
    files = []

    for filename in listdir(sourcedirectory+directoryName):
        #le fichier SWBD a un architecture spécifique
        if directoryName == 'SWBD':
            for swbdDirectory in listdir(sourcedirectory + directoryName+'/'+filename):
                for file in listdir(sourcedirectory + directoryName+'/'+filename+'/'+swbdDirectory):
                    currentFile = File.File(sourcedirectory + directoryName+'/'+filename+'/'+swbdDirectory+'/'+file
                                            , newCorpus.delimiter)
                    files.append(currentFile)
            break
        currentFile = File.File(sourcedirectory+directoryName+"/"+filename, newCorpus.delimiter)
        files.append(currentFile)

    newCorpus.addElements(files)
    corpuses.append(newCorpus)


def createBoxPlot(corpusToAnalyze):
    global boxplotHandle
    global boxplot
    global previousrectangles
    global previousSegment
    global data_source
    global rect_data_source
    # data regarding corpuses boxplot style
    xAxisData = []
    mins = []
    maxs = []
    q1 = []
    q3 = []
    for corpus in corpuses:
        if corpus.name in corpusToAnalyze:
            timeByFile = pd.Series(corpus.getDurations())
            timeByFile /= 60
            xAxisData.append(corpus.name)
            mins.append(timeByFile.min())
            maxs.append(timeByFile.max())
            q1.append(timeByFile.quantile(0.25))
            q3.append(timeByFile.quantile(0.75))
        if data_source == 0:
             data_source = ColumnDataSource(data=dict(x=xAxisData, top=maxs, bottom=mins))
             rect_data_source = ColumnDataSource(data=dict(x=xAxisData, top=q3, bottom=q1))
        else:
            data_source.data = {'x':xAxisData, 'top':maxs, 'bottom':mins}
            rect_data_source.data = {'x':xAxisData, 'top':q3, 'bottom':q1}

    if boxplot == 0:
        boxplot = figure(x_range=xAxisData, title="durée des conversations en minutes", tools="")
        segments = VBar(x="x", top="top", bottom="bottom", width=0.01, fill_color="black")  # segments
        rectangles = VBar(x="x", top="top", bottom="bottom", width=0.1, fill_color="red")  # rectangles
        boxplot.add_glyph(data_source, segments)
        boxplot.add_glyph(rect_data_source, rectangles)




    if boxplotHandle == 0:
        boxplotHandle = show(boxplot, notebook_handle=True)
    else:
        push_notebook(handle=boxplotHandle)



# display checkbox
CID = widgets.Checkbox(
    value=True,
    description='CID'
)
DVD = widgets.Checkbox(
    value=True,
    description='DVD'
)
MTX = widgets.Checkbox(
    value=True,
    description='MTX'
)
SWBD = widgets.Checkbox(
    value=True,
    description='SWBD'
)

corpusInputs = []
corpusInputs.append(CID)
corpusInputs.append(DVD)
corpusInputs.append(MTX)
corpusInputs.append(SWBD)

def corpusSelection(b):
    if type(b.new) == type(True):  # permet de limiter à une activation par changement
        corpusToAnalyze = []
        for corpusCheckbox in corpusInputs:
            if corpusCheckbox.value:
                corpusToAnalyze.append(corpusCheckbox.description.encode("utf-8"))
            else:
                if corpusCheckbox.description in corpusToAnalyze: corpusToAnalyze.remove(
                    corpusCheckbox.description.encode("utf-8"))
        createBoxPlot(corpusToAnalyze)


CID.observe(corpusSelection)
DVD.observe(corpusSelection)
MTX.observe(corpusSelection)
SWBD.observe(corpusSelection)
display(CID, DVD, MTX, SWBD)

corpusToDisplay = []
for corpus in corpuses:
    corpusToDisplay.append(corpus.name)

createBoxPlot(corpusToDisplay)





