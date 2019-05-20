#!/usr/bin/env python3
# coding: utf-8

'''
Perform clustering based on a distance matrix.

External dependencies, to be installed e.g. via pip:
- gurobi v8.1.1

NB: Niraj's solver works with python3 only.

Author: Luis A. Leiva <luis.leiva@aalto.fi>
'''

import sys
import os

import numpy as np
from sklearn.cluster import SpectralClustering

np.random.seed(0)

labels = None
matrix = []
linsep = '\t'
with open(sys.argv[1]) as f:
    for i, line in enumerate(f.read().splitlines()):
        if i == 0:
            labels = line.split(linsep)
        else:
            distances = map(float, line.split(linsep))
            matrix.append(list(distances))
matrix = np.array(matrix)
# Apply RBF kernel to adjacency matrix.
delta = matrix.max() - matrix.min()
X = np.exp(-matrix ** 2 / (2. * delta ** 2))

sc = SpectralClustering(3, affinity='precomputed', random_state=0).fit(X)

print(labels)
print(sc.labels_)
