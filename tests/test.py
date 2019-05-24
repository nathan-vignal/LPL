from source.RadarGraph import RadarGraph
import numpy as np
from bokeh.io import output_notebook
import time
output_notebook()
radar = RadarGraph()
text = ['lexical richness max :0.326', 'ratio filling pause max :0.039', 'ratio feedback max :0.305'
    , 'taille moyenne Ipu non feedback max :8.699', 'familiar language max :5.677']

flist = [np.array([0.45669999, 1, 0.47506903, 0.96134016, 1])
    ,np.array([1, 0.58196036, 1, 1, 0.37513551])]

radar.createRadarGraph(text, flist)
radar.update()

time.sleep(2)

text = ['lexical richness max :0.326', 'ratio filling pause max :0.023', 'ratio feedback max :0.305', 'taille moyenne Ipu non feedback max :8.699', 'familiar language max :2.130']
flist =[np.array([1, 1, 1, 1, 1])]
radar.createRadarGraph(text, flist)
radar.update()


time.sleep(2)

text = ['lexical richness max :0.326', 'ratio filling pause max :0.039', 'ratio feedback max :0.305', 'taille moyenne Ipu non feedback max :8.699', 'familiar language max :5.677']
flist = [np.array([0.45669999, 1, 0.47506903, 0.96134016, 1]), np.array([1, 0.58196036, 1, 1, 0.37513551])]
radar.createRadarGraph(text, flist)
radar.update()




