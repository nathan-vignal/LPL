
def initCorpusCheckBox():
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
        if type(b.new) == type(True) : # permet de limiter à une activation par changement 
            corpusToAnalyze = []
            for corpusCheckbox in corpusInputs :
                if corpusCheckbox.value:
                    corpusToAnalyze.append(corpusCheckbox.description.encode("utf-8"))
                else :
                    if corpusCheckbox.description in corpusToAnalyze: corpusToAnalyze.remove(corpusCheckbox.description.encode("utf-8"))
            print(corpusToAnalyze) 


    CID.observe(corpusSelection)
    DVD.observe(corpusSelection)
    MTX.observe(corpusSelection)
    SWBD.observe(corpusSelection)
    display(CID,DVD, MTX,SWBD)
    
    
def createNbLinesFigure(corpuses):
    yAxisData = []
    xAxisData = []
    for corpus in corpuses:
        xAxisData.append(corpus.name)
        yAxisData.append(corpus.getNbOfLines())

    # colors = [colormap[x] for x in flowers['species']]

    nbLinesFigure = figure(x_range=xAxisData, plot_height=250, title="Corpuses lines",
                           toolbar_location=None, tools="")

    nbLinesFigure.vbar(x=xAxisData, top=yAxisData, width=0.9)

    nbLinesFigure.xgrid.grid_line_color = None
    nbLinesFigure.y_range.start = 0
    return nbLinesFigure


sourcedirectory = "C:/Users/vignal/Documents/corpus/"
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

#####corpuses lines bar chart style
yAxisData = []
xAxisData = []
for corpus in corpuses:
    xAxisData.append(corpus.name)
    yAxisData.append(corpus.getNbOfLines())

nbLinesFigure = figure(x_range=xAxisData, plot_height=250, title="Corpuses lines",
                       toolbar_location=None, tools="")

nbLinesFigure.vbar(x=xAxisData, top=yAxisData, width=0.8)

nbLinesFigure.xgrid.grid_line_color = None
nbLinesFigure.y_range.start = 0

nbLinesFigure = createNbLinesFigure(corpuses)

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

boxplot.vbar(x=xAxisData, top=max, bottom=mins, width=0.01, fill_color="black") #segments
boxplot.vbar(x=xAxisData, top=q3, bottom=q1, width=0.1, fill_color="red")#rectangles

f = gridplot([[nbLinesFigure], [boxplot]])





show(f)