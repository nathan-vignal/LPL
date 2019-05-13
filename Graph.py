from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.glyphs import VBar
from bokeh.models.tools import HoverTool, WheelZoomTool, PanTool
import numpy as np
from bokeh.models.annotations import Title
from bokeh.plotting import figure
from bokeh.io import show, push_notebook
import math

class Graph:

    def __init__(self, title=None):
        """
        create an instance of Graph that contain a empty figure
        :param title:
        """

        self.__figure = figure(x_range=[], title=title, tools="")
        self.__handler = None  # wil host the handler to push the notebook
        self.__glyphs = {}

    def addGlyph(self, name, glyphType, model, option1=None, option2=None):
        """
        create a new glyph and add it to the figure
        :param name:
        :param glyphType: determine what type of glyp this function will create
        :param option1: width of the bar
        :param option2: color of the bar
        :return:
        """
        if name in self.__glyphs:
            print("glyph name already taken")
            return -1
        if glyphType == "VBar":
            if option1 is None:
                option1 = 0.1
            if option2 is None:
                option2 = "black"

            temp = []
            temp.append(VBar(x="x", top="top", width=option1, fill_color=option2))
            temp.append(ColumnDataSource(data=dict(x=[], top=[])))
            temp.append(model)
            self.__figure.add_glyph(temp[1], temp[0])
            self.__glyphs[name] = temp

        elif glyphType == "VBarQuartile":
            if option1 is None:
                option1 = 0.1
            if option2 is None:
                option2 = "black"
            temp = []
            temp.append(VBar(x="x", bottom="bottom", top="top", width=option1, fill_color=option2))
            temp.append(ColumnDataSource(data=dict(x=[], bottom=[], top=[])))
            temp.append(model)
            self.__figure.add_glyph(temp[1], temp[0])
            self.__glyphs[name] = temp

    # --------------------------------------------------------------------------------------------------------

    def setXAxis(self, xAxis):
        """
        change the xAxis values for this graph
        :param xAxis:
        """
        self.__figure.x_range.factors = xAxis

    # --------------------------------------------------------------------------------------------------------

    def setTitle(self, newTitle):
        """
        change the title of the graph
        :param newTitle:
        """
        title = Title()
        title.text = newTitle
        self.__figure.title = title

    # --------------------------------------------------------------------------------------------------------

    def getGlyphNames(self):
        """
        get all the glyphs names for the glyphs inside the graph
        :return:
        """
        temp = []
        for key in self.__glyphs:
            temp.append(key)
        return temp

    # --------------------------------------------------------------------------------------------------------

    def getGlyph(self,name):
        """
        get the associated glyph given the name
        :param name: str
        :return:
        """
        if name not in self.__glyphs:
            print("glyph name doesn't exist")
            return -1
        return self.__glyphs[name]

    # --------------------------------------------------------------------------------------------------------

    def changeGlyph(self, name, x, y, bottom=None):
        """
        change variable inside the glyphs with the given name
        :param name: str
        :param x: [values] each value must be inside the xAxis values
        :param y: [number,....,number]
        :param bottom: [number,....,number]
        :return:
        """
        if not(isinstance(x, list) and isinstance(y, list)):
            print("x and y must be lists. in :changeGlyph")
        if name not in self.__glyphs:
            print("glyph name doesn't exist")
            return -1
        if bottom is None:
            self.__glyphs[name][1].data.update(x=x, top=y)
        else:
            self.__glyphs[name][1].data.update(x=x, bottom=bottom, top=y)

    # ---------------------------------------------------------------------------------

    def update(self):
        for glyphName in self.__glyphs:
            model = self.__glyphs[glyphName][2]
            #print(model.getY())
            #print(model.getX())
            if "segment" in glyphName:
                self.changeGlyph(glyphName, model.getX(), model.getY(), model.getBottom())
            elif "barre" in glyphName:
                self.changeGlyph(glyphName, model.getX(), model.getQ3(), model.getQ1())
            else:

                self.__figure.add_tools(HoverTool())
                self.__figure.add_tools(WheelZoomTool())
                self.__figure.add_tools(PanTool())


                self.changeGlyph(glyphName, model.getX(), model.getY())
                plotYvalues = model.getY()
                plotXvalues = model.getX()
                xy = zip(plotYvalues, plotXvalues)

                xy = sorted(xy, key= lambda y: y[0])
                print()

                self.setXAxis([i[1] for i in xy])#[i[0] for i in xy])

                print("changed values")
                #self.changeGlyph(glyphName, ['CID', 'DVD', 'Fisher', 'MTX', 'SWBD'], [1424, 670, 163, 116, 229])

            #self.setXAxis(sorted(list(model.getX())))

            #self.setXAxis(list(model.getXAxisSet()))






        if self.__handler is None:
            print("showing graph")
            self.__handler = show(self.__figure, notebook_handle=True)
        else:
            print("pushing notebook")
            push_notebook(handle=self.__handler)

#-----------------end class------------------

