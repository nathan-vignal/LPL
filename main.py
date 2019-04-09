from bokeh.plotting import figure, show, output_file, gridplot
import pandas as pd
from os import listdir
import math
import Corpus
import File

def createNbLinesFigure(corpuses):
    yAxisData = []
    xAxisData = []
    for corpus in corpuses:
        xAxisData.append(corpus.name)
        yAxisData.append(corpus.getNbOfLines())

    # colors = [colormap[x] for x in flowers['species']]

    output_file("experimentation.html")
    nbLinesFigure = figure(x_range=xAxisData, plot_height=250, title="Corpuses lines",
                           toolbar_location=None, tools="")

    nbLinesFigure.vbar(x=xAxisData, top=yAxisData, width=0.9)

    nbLinesFigure.xgrid.grid_line_color = None
    nbLinesFigure.y_range.start = 0
    return nbLinesFigure


def createBoxplot(toDisplay,corpuses):

    #####corpuses lines bar chart style
    yAxisData = []
    xAxisData = []
    for corpus in corpuses:
        if corpus.name in toDisplay:
            xAxisData.append(corpus.name)
            yAxisData.append(corpus.getNbOfLines())


    ####number of lines in the corpuses boxplot style
    boxplot = figure(x_range=xAxisData, title="durée des conversations en secondes", tools="")
    mins = []
    max = []
    q1 = []
    q3 = []

    for corpus in corpuses:
        timeByFile = pd.Series(corpus.getDurations())

        mins.append(timeByFile.min())
        max.append(timeByFile.max())
        q1.append(timeByFile.quantile(0.25))
        q3.append(timeByFile.quantile(0.75))

    boxplot.vbar(x=xAxisData, top=max, bottom=mins, width=0.01, fill_color="black")  # segments
    boxplot.vbar(x=xAxisData, top=q3, bottom=q1, width=0.1, fill_color="red")  # rectangles
    return boxplot


sourcedirectory = "C:/Users/vignal/Documents/corpus/"
colormap = {'CID': 'red', 'DVD': 'green', 'MTX': 'blue', 'SWBD':'black'}
corpuses = []
corpusToAnalyze = ['CID', 'DVD', 'MTX']
#init corpuses from the source directory
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


f = gridplot([[createBoxplot(corpusToAnalyze, corpuses)]])
show(f)
'''
#### pie chart of total corpus duration
sumDuration = []
for corpus in corpuses:
    time = pd.Series(corpus.getDurations()).sum()
    sumDuration.append(math.floor(time/60))

data = pd.Series(sumDuration).reset_index(name='value').rename(columns={'index':'corpus'})
data['angle'] = data['value']/data['value'].sum() * 2* math.pi

data['color'] = ["red","blue", "green"]
print(data)

pieChart = figure(plot_height=380, title="total temps par corpus", toolbar_location=None,
           tools="hover",  x_range=(-0.5, 1.0))#tooltips="@country: @value""
pieChart.axis.axis_label=None
pieChart.axis.visible=False
pieChart.grid.grid_line_color = None
pieChart.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='CID', source=data)
f = gridplot([[nbLinesFigure], [boxplot,pieChart]])
show(f)

'''


