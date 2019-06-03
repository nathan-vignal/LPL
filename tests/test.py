from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
from source.pathManagment import getPathToSerialized
from os import path
import pickle


f = open(path.join(getPathToSerialized(), "swbdDataframeBySpeaker"), "rb")
dataframe = pickle.load(f)
f.close()


dataframe = dataframe.drop(columns="label")
print(dataframe)

# create new plot and data
plt.plot()
X = dataframe
colors = ['b', 'g', 'r']
markers = ['o', 'v', 's']

# k means determine k
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# Plot the elbow
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()