from bokeh.models import ColumnDataSource, LabelSet, DataRange1d
from bokeh.models.glyphs import VBar, Circle
from bokeh.models.tools import HoverTool, WheelZoomTool, PanTool, TapTool
import numpy as np
from bokeh.models.callbacks import CustomJS
from bokeh.models.annotations import Title
from bokeh.plotting import figure, curdoc
from bokeh.io import show, push_notebook
from bokeh.models import CustomJS, Div
import math
from bokeh.models import Legend, LegendItem
from bokeh import events


class Graph:

    def __init__(self, title=None, tools="", iscontinuous=False):
        """
        create an instance of Graph that contain a empty figure
        :param title:
        """
        if "hover" in tools:
            tools = tools.replace(",hover", "")
            tools = tools.replace("hover,", "")
            tools = tools.replace("hover", "")




        # , y_axis_type = y_axis_type   # use this to try and set
        if iscontinuous:
            self.__figure = figure( title=title, tools=tools)

        else:
            self.__figure = figure(x_range=[], title=title, tools=tools)
        hover = HoverTool(tooltips=[
            ("(x,y)", "(@x,@top)")
        ])
        self.__figure.add_tools(hover)




        self.__handler = None  # wil host the handler to push the notebook
        self.__glyphs = {}
        self.__tools = tools
        self.__figure.legend.location = "top_left"
        self.__figure.legend.click_policy = "hide"

    def addGlyph(self, name, glyphType, model, option1=None, option2=None, option3=None):
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

        if glyphType == "VBar":  # bar plot
            if option1 is None:
                option1 = 0.1
            if option2 is None:
                option2 = "black"

            temp = []
            temp.append(VBar(x="x", top="top", width=option1, fill_color=option2))
            temp.append(ColumnDataSource(data=dict(x=[], top=[])))
            temp.append(model)
            self.__figure.add_glyph(temp[1], temp[0])
            temp.append(glyphType)
            self.__glyphs[name] = temp

        elif glyphType == "VBarQuartile":  # quartile plot
            if option1 is None:
                option1 = 0.1
            if option2 is None:
                option2 = "black"
            temp = []
            temp.append(VBar(x="x", bottom="bottom", top="top", width=option1, fill_color=option2))
            temp.append(ColumnDataSource(data=dict(x=[], bottom=[], top=[])))
            temp.append(model)
            self.__figure.add_glyph(temp[1], temp[0])
            temp.append(glyphType)
            self.__glyphs[name] = temp

        elif glyphType == "scatter":  # scatter plot
            if option1 is None:
                option1 = 0.1

            temp = []
            temp.append(Circle(x="x", y="top", size=option1, fill_color="fill_color"))
            temp.append(ColumnDataSource(data=dict(x=[], top=[], fill_color=[], legend=[])))
            temp.append(model)
            self.__figure.circle(x="x", y="top", size=option1, fill_color="fill_color", legend="legend", source=temp[1]
                                 ,line_width=0)
            #self.__figure.add_glyph(temp[1], temp[0])
            temp.append(glyphType)
            self.__glyphs[name] = temp

    # --------------------------------------------------------------------------------------------------------

    def setXAxis(self, xAxis):
        """
        change the xAxis values for this graph
        :param xAxis:
        """
        if isinstance(xAxis, list):
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

    def changeGlyph(self, name, x, y, bottom=None, colors=None, tooltips=None, legend=None):
        """
        change variable inside the glyph with the given name
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
        glyphData = self.__glyphs[name]

        type = glyphData[3]
        if type == "VBar":
            glyphData[1].data.update(x=x, top=y, hover=y)

        elif type == "VBarQuartile":
            glyphData[1].data.update(x=x, bottom=bottom, top=y, hover=y)

        elif type == "scatter":
            "came in scatter"
            if colors == None:
                colors = ["black" for i in range(0,len(x))]
            legend = list(legend)

            glyphData[1].data.update(x=x, top=y, fill_color=colors, legend=legend)

            # renderer = self.__figure.renderers[0]
            # l = []

            # for word in legend:
            #     l.append(LegendItem(label=word, renderers=[renderer], index=legend[word]))
            # legend = Legend(items=l)
            # self.__figure.legend.clear()
            # print(self.__figure.legend)
            # self.__figure.add_layout(legend)


        else:
            print("unknown glyph type in Graph.py")

        # tooltips managment
        if tooltips is not None:
            glyphData[1].data.update(tooltips)  # add new tooltips to the source

            #  [ ("(x,y)", "(@x,@top)")] the figure tools must look like that
            #  [ (firstPart, SecondPart)]

            secondPart = "(@"
            keys = list(glyphData[1].data.keys())
            keys.remove("fill_color")
            for key in keys:
                secondPart += key + ",@"
            if secondPart[-1] == "@":  # removing the last
                secondPart = secondPart[:-2]
            secondPart += ")"
            firstPart = secondPart.replace("@", "")
            self.changeToolTips([(firstPart, secondPart)])

    # ---------------------------------------------------------------------------------

    def update(self):
        """
        function handling getting the infos needed from the model and updating the display
        :return:
        """
        for glyphName in self.__glyphs:
            model = self.__glyphs[glyphName][2]
            type = self.__glyphs[glyphName][3]

            if type == "VBar":
                self.changeGlyph(glyphName, model.getX(), model.getY())
            elif type == "VBarQuartile":
                if "segment" in glyphName:
                    self.changeGlyph(glyphName, model.getX(), model.getY(), model.getBottom())
                else:
                    self.changeGlyph(glyphName, model.getX(), model.getQ3(), model.getQ1())
            elif type == "scatter":
                self.changeGlyph(glyphName, model.getX(), model.getY()
                                 , colors=model.getColors()
                                 , tooltips=model.getTooltips()
                                 ,legend=model.getLegend())

            else:
                print("graph.py unkown glyphtype")

            if type != "scatter":
                self.setXAxis(list(model.getXAxis()))
            else:
                self.setXAxis("auto")

        if self.__handler is None:
            self.__handler = show(self.__figure, notebook_handle=True)

        else:
            push_notebook(handle=self.__handler)

    # -----------------end class------------------

    def changeToolTips(self, newToolTips):
        for item in self.__figure.tools:
            if isinstance(item, HoverTool):
                item.tooltips = newToolTips
                break

    def legend(self):
        pass
        # legend = Legend(items=[
        #     LegendItem(label="orange", renderers=[r], index=0),
        #     LegendItem(label="red", renderers=[r], index=1),
        # ])
        #
        # self.__figure.add_layout(legend)

    def RUSH_HIGHLIGHT_SPEAKERS(self, ids):
        """
        done for the contest must not be used in the long term
        :return:
        """
        data = None
        for name in self.__glyphs:
            data = self.__glyphs[name][1].data
            break
        position = []
        for id in ids:
            position.append(data["speakerID"].index(id))

        colors = data["fill_color"]
        for pos in position:
            colors[pos] = "red"
        for name in self.__glyphs:
            self.__glyphs[name][1].data["fill_color"] = colors
            break
        push_notebook(handle=self.__handler)













'''
"""
            var attrs = %s; var args = [];
            for (var i = 0; i<attrs.length; i++) {
                args.push(attrs[i] + '=' + Number(cb_obj[attrs[i]]).toFixed(2));
            }
            var line = "<span style=%r><b>" + cb_obj.event_name + "</b>(" + args.join(", ") + ")</span>\\n";
            var text = div.text.concat(line);
            var lines = text.split("\\n")
            if (lines.length > 35)
                lines.shift();
            div.text = lines.join("\\n");
        """ % (attributes, style)
        
'''
