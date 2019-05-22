from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.glyphs import VBar
from bokeh.models.tools import HoverTool, WheelZoomTool, PanTool
import numpy as np
from bokeh.models.annotations import Title
from bokeh.plotting import figure
from bokeh.io import show, push_notebook
import math

class Graph:

    def __init__(self, title=None, tools="", y_axis_type="auto"):
        """
        create an instance of Graph that contain a empty figure
        :param title:
        """
        if "hover" in tools:
            tools = tools.replace(",hover", "")
            tools = tools.replace("hover,", "")
            tools = tools.replace("hover", "")
        #, y_axis_type = y_axis_type   # use this to try and set
        self.__figure = figure(x_range=[], title=title, tools=tools)
        hover = HoverTool(tooltips=[
            ("(x,y)", "(@x,@top)")
        ])
        self.__figure.add_tools(hover)
        self.__handler = None  # wil host the handler to push the notebook
        self.__glyphs = {}
        self.__tools = tools

    def addGlyph(self, name, glyphType, model, option1=None, option2=None):
        """
        create a new glyph and add it to the figure
        :param name: will change behavior in Graph.update
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
            return
        if name not in self.__glyphs:
            print("glyph name doesn't exist")
            return
        if bottom is None:
            self.__glyphs[name][1].data.update(x=x, top=y, hover=y)
        else:
            self.__glyphs[name][1].data.update(x=x, bottom=bottom, top=y, hover=y)

    # ---------------------------------------------------------------------------------

    def update(self):
        for glyphName in self.__glyphs:
            model = self.__glyphs[glyphName][2]
            if "segment" in glyphName:
                self.changeGlyph(glyphName, model.getX(), model.getY(), model.getBottom())
            elif "barre" in glyphName:
                self.changeGlyph(glyphName, model.getX(), model.getQ3(), model.getQ1())
            elif "column" in glyphName:
                self.changeGlyph(glyphName, model.getX(), model.getY())
            else:
                print("graph.py unkown glyphtype")

            self.setXAxis(list(model.getXAxis()))


        if self.__handler is None:

            self.__handler = show(self.__figure, notebook_handle=True)

        else:
            push_notebook(handle=self.__handler)

    # -----------------end class------------------

