from __future__ import print_function
from IPython.display import display
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
import ipywidgets as widgets
from bokeh.plotting import figure, output_file, gridplot
from bokeh.io import output_notebook, show, push_notebook
import pandas as pd
from os import listdir
import Corpus
import File
import Fisher
import FileWithSpeaker

xrange = ["Marseille","Tamere"]
f = figure()
discrPlot = figure(x_range=xrange)
discrPlot_source = ColumnDataSource(data=dict(x=xrange, y=[1, 2]))
bars = VBar(x="x", top="y", width=0.1, fill_color="black")  # segments
discrPlot.add_glyph(discrPlot_source, bars)
show(discrPlot)#, notebook_handle=True
f.add_glyph(discrPlot_source, discrPlot)

#push_notebook(handle=discrPlotHandler)



