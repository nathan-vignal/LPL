import os.path
import pandas as pd
from source.pathManagment import getOriginePath
file = pd.read_pickle(os.path.join(getOriginePath(),"source", "Simone", "output", "X20", "X.pkl"))