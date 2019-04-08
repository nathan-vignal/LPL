from bokeh.plotting import figure, show, output_file, gridplot
from bokeh.sampledata.iris import flowers

#from bokeh.charts import BoxPlot, output_file, show
from bokeh.layouts import row
from os import listdir
import csv
import Corpus
import File

def createNbLinesFigure(corpuses):
    yAxisData = []
    xAxisData = []
    for corpus in corpuses:
        xAxisData.append(corpus.name)
        yAxisData.append(corpus.getNbOfLines())

    # colors = [colormap[x] for x in flowers['species']]

    output_file("bars.html")
    nbLinesFigure = figure(x_range=xAxisData, plot_height=250, title="Corpuses lines",
                           toolbar_location=None, tools="")

    nbLinesFigure.vbar(x=xAxisData, top=yAxisData, width=0.9)

    nbLinesFigure.xgrid.grid_line_color = None
    nbLinesFigure.y_range.start = 0
    return nbLinesFigure


sourcedirectory = "C:/Users/vignal/Documents/Nathan/Nathan"
delimiter = {'CID': ' ', 'DVD': ',', 'MTX': ','}
colormap = {'CID': 'red', 'DVD0': 'green', 'MTX': 'blue'}
corpuses = []

for directoryName in listdir(sourcedirectory):
    if directoryName != "SWBD":
        newCorpus = Corpus.Corpus(directoryName, sourcedirectory + "/" + directoryName, directoryName)
        currentDelimiter = newCorpus.delimiter
        files = []

        for filename in listdir(sourcedirectory+"/"+directoryName):
            currentFile = File.File(sourcedirectory+"/"+directoryName+"/"+filename, newCorpus.delimiter)
            files.append(currentFile)

        newCorpus.addElements(files)
        corpuses.append(newCorpus)


yAxisData = []
xAxisData = []
for corpus in corpuses:
    xAxisData.append(corpus.name)
    yAxisData.append(corpus.getNbOfLines())

#colors = [colormap[x] for x in flowers['species']]

output_file("bars.html")
nbLinesFigure = figure(x_range=xAxisData, plot_height=250, title="Corpuses lines",
                       toolbar_location=None, tools="")

nbLinesFigure.vbar(x=xAxisData, top=yAxisData, width=0.9)

nbLinesFigure.xgrid.grid_line_color = None
nbLinesFigure.y_range.start = 0

nbLinesFigure = createNbLinesFigure(corpuses)


f = gridplot([[nbLinesFigure], [None]])
show(nbLinesFigure)





"""
for filename in listdir(directory):
    with open(directory + filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        line_count = 0
        for row in csv_reader:
            line_count += 1
    print(f'The file {filename} contains {line_count} lines.')
"""
