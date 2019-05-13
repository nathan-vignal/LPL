from Graph import Graph
import ipywidgets as widgets
from IPython.display import display
class Cell:

    def __init__(self):
        self.__graphs = {}
        self.__text = ""
        self.__inputs = {}
        self.__HBox = widgets.HBox()
        self.__models = {}

    def addGraph(self,name, graph):
        if isinstance(graph, Graph):
            self.__graphs[name] = graph
        else:
            print("addGraph require a grap not a"+str(type(graph)))

    def changeText(self, newText, resetText=True):
        if resetText:
            self.__text = newText
        else:
            self.__text += newText

    def addInput(self, name, input):
        if name in self.__inputs:
            print("name already taken :" + str(name))
            return -1
        self.__inputs[name] = input
        self.__HBox.children = [self.__inputs[x].getWidget() for x in self.__inputs]

    def addModel(self, name, model):
        if name in self.__models:
            print("name already taken :" + str(name))
            return -1
        self.__models[name] = model

    def updateDisplay(self):
        display(self.__HBox)


    # def linkInputToModel(self, inputName, modelName, linkType):
    #     self.__inputs[inputName].onChange(self.__models[modelName], linkType)
    #










