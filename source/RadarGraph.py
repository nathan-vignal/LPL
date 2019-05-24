from bokeh.models import ColumnDataSource, LabelSet
import numpy as np
from bokeh.plotting import figure
from bokeh.io import show, push_notebook
import math

class RadarGraph:

    def __init__(self, colors=None, title=None):
        self.__plot = None
        self.__handler = None
        if colors is None:
            self.__colors = ["black", "blue", "red", "yellow", "green",
                             "purple", "white", "brown", "orange", "pink", "black"]
        else:
            self.__colors = colors

        if title is None:
            self.__title = "radar graph"
        else:
            self.__title = title

    def update(self):
        if self.__handler == None:
            self.__handler = show(self.__plot, notebook_handle=True)
        else:
            show(self.__plot)
            push_notebook(handle=self.__handler)

    def createRadarGraph(self, text, flist, title=None, colors=None):
        """
        create a radar graph
        :param center: where should the center of the graph be
        :param title:  str
        :param text: [str] title for each vertex of the graph
        :param flist: [nparray[float]]
        :param colors:[str]color for each data family
        :return:
        """

        # if the plot has already been displayed
        if self.__plot is not None:
            toDelete = self.__plot.select({'name': 'toDelete'})
            for glyph in toDelete:
                if glyph.visible:
                    glyph.visible = False


        if flist == []:
            print("empty data in crearteRadarGraph")
            return
        if colors is None:
            colors = self.__colors

        if title is None:
            title = self.__title



        def unit_poly_verts(theta, center):
            """Return vertices of polygon for subplot axes.
            This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
            """
            x0, y0, r = [center] * 3
            verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
            return verts

        def radar_patch(r, theta, center):
            """ Returns the x and y coordinates corresponding to the magnitudes of
            each variable displayed in the radar plot
            """
            # offset from centre of circle
            offset = 0
            yt = (r * center + offset) * np.sin(theta) + center
            xt = (r * center + offset) * np.cos(theta) + center
            return xt, yt

        def drawRadar(x1, y1, p, nbOfRulerSegment):
            """
            :param x1: [float] x of the axis end point
            :param y1: [float] y of the axis end point
            :param p: bokeh figure in which to display the segments
            :param nbOfRulerSegment: number of lines in each ruler
            :return:
            """
            origine = 0.5
            ticSize = 0.01
            for i in range(0, len(x1)):
                p.segment(x0=origine, y0=origine, x1=x1[i],
                          y1=y1[i], color="black", line_width=1)
                if x1[i] == origine:
                    x1[i] = origine + 0.001  # prevent deviding by 0
                if y1[i] == origine:
                    y1[i] = origine + 0.001  # prevent deviding by 0
                leadingCoefficient = (y1[i]-origine)/(x1[i]-origine)
                leadingCoefficientRuler = -(1/leadingCoefficient)
                deltaX = x1[i] - origine
                deltaY = y1[i] - origine
                rulerX0 = []
                rulerX1 = []
                rulerY0 = []
                rulerY1 = []

                # some quick maths: solving (a*x)^2 +x^2 - tickSize^2 = 0  -> pythagore theorem
                a = (leadingCoefficientRuler**2)+1
                c = -(ticSize**2)
                # b is equal to 0
                delta = - (4 * a * c)  # b^2 - 4*a*c
                if delta == 0:  # prevent sqrt(0)
                    delta = 0.001
                solution = math.sqrt(delta)/(2*a)
                for i in range(1, nbOfRulerSegment):
                    centreX = origine + ((float(i)/float(nbOfRulerSegment)) * deltaX)
                    centreY = origine + ((float(i)/float(nbOfRulerSegment)) * deltaY)

                    rulerX0.append(centreX + solution)
                    rulerX1.append(centreX - solution)
                    rulerY0.append(centreY + solution * leadingCoefficientRuler)
                    rulerY1.append(centreY - solution * leadingCoefficientRuler)

                p.segment(x0=rulerX0, y0=rulerY0, x1=rulerX1, y1=rulerY1, color="black", line_width=0.5)

        center = 0.5
        text.append("")
        nbVar = len(flist[0])

        theta = np.linspace(0, 2 * np.pi, nbVar, endpoint=False)
        # rotate theta such that the first axis is at the top
        theta += np.pi / 2

        verts = unit_poly_verts(theta, center)
        x = [v[0] for v in verts]
        y = [v[1] for v in verts]
        if self.__plot is None:
            self.__plot = figure(title=title, tools="")
            drawRadar(x, y, self.__plot, 10)

        for i in range(0, len(verts)):
            self.__plot.segment(x0=0.5, y0=0.5, x1=x[i],
                                y1=y[i], color="black", line_width=1, name='toDelete')
        source = ColumnDataSource({'x': x + [center], 'y': y + [1], 'text': text})

        labels = LabelSet(x="x", y="y", text="text", source=source, name='toDelete')

        self.__plot.add_layout(labels)

        for i in range(len(flist)):
            xt, yt = radar_patch(flist[i], theta, center)

            self.__plot.patch(x=xt, y=yt, fill_alpha=0.15, fill_color=colors[i], name='toDelete')


