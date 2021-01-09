import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import random
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering

N = 100
K = 2000
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'pink', 'black']
dataset = pd.read_csv('CAvideos.csv')
X = dataset.iloc[:K, [8, 9]]
# X = X[X['likes'] >= 10000]
X = X.values
# print(X)


def dist(n1, n2, array1, array2):
    return ((array1[n1][0]-array2[n2][0])**2 + (array1[n1][1]-array2[n2][1])**2)**(1/2)


def recreate_centroids(array_clusters, array_centroids):
    n = len(array_clusters)
    for ja in range(n):
        sum_x = 0
        sum_y = 0
        if array_clusters[ja]:
            for element in array_clusters[ja]:
                sum_x += element[0]
                sum_y += element[1]
            array_centroids[ja] = [sum_x / len(array_clusters[ja]), sum_y / len(array_clusters[ja])]


def distribute(X0, array_clusters, array_centroids):
    for cluster in clusters:
        cluster.clear()
    for num_point in range(len(X0)):
        distances = [float('inf') for z in range(len(array_centroids))]
        for num_centroid in range(len(centroids)):
            distances[num_centroid] = dist(num_point, num_centroid, X0, array_centroids)
        array_clusters[distances.index(min(distances))].append(X0[num_point])


def get_hash(array_2d):
    summa = 0
    for tochka in array_2d:
        summa += (tochka[0]+tochka[1])
    return summa


"""STEP 0 - Defining possible number of clusters"""
"""
dendrogram = sch.dendrogram(sch.linkage(X, method="ward"))
plt.title('Likes-dislikes')
plt.xlabel('likes')
plt.ylabel('Dislikes')
plt.show()
# seems like 7 clusters is just about right
"""
n_clusters = 7

"""STEP 1 - Hierarchical clustering"""
# create small sample of original data for hierarchical clustering
little_sample = []
for i in range(N):
    j = round(K * random())
    little_sample.append([X[j][0], X[j][1]])
# implement hierarchical clustering


hc = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
y_hc = hc.fit_predict(little_sample)
clusters = [[] for i in range(n_clusters)]
for i in range(len(y_hc)):
    clusters[y_hc[i]].append(little_sample[i])
# show clusters for little_sample
"""
for i in range(n_clusters):
    print(clusters[i])
for i in range(N):
    plt.scatter(little_sample[i][0], little_sample[i][1], c=colors[y_hc[i]])
plt.show()
"""

"""STEP 2 - k-means clustering based on gotten clusters"""
# get primal centroids
centroids = [[] for i in range(n_clusters)]
recreate_centroids(clusters, centroids)
# print(len(clusters), len(clusters[0]))
# generate first region distribution
distribute(X, clusters, centroids)
# print(len(clusters), len(clusters[0]))

hash_old = get_hash(centroids)
recreate_centroids(clusters, centroids)
distribute(X, clusters, centroids)
hash_new = get_hash(centroids)
i = 0
while i < 50 and hash_old != hash_new:
    i += 1
    hash_old = hash_new
    recreate_centroids(clusters, centroids)
    distribute(X, clusters, centroids)
    hash_new = get_hash(centroids)
# print(i)
"""STEP 3 - show result"""

for i in range(n_clusters):
    print(len(clusters[i]))
    for point in clusters[i]:
        plt.scatter(point[0], point[1], s=3, c=colors[i])
plt.title('Likes-dislikes of popular Youtube videos')
plt.xlabel('likes')
plt.ylabel('Dislikes')
plt.show()

"""Comparison with built-in hierarchical clustering"""
"""
hc = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
y_hc = hc.fit_predict(X)
clusters = [[] for i in range(n_clusters)]
for i in range(len(y_hc)):
    clusters[y_hc[i]].append(X[i])

for i in range(K):
    plt.scatter(X[i][0], X[i][1], s=3, c=colors[y_hc[i]])
plt.title('Likes-dislikes of popular Youtube videos')
plt.xlabel('likes')
plt.ylabel('Dislikes')
plt.show()
"""