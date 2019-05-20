#!/usr/bin/env python -W ignore::DeprecationWarning
# coding: utf-8

'''
Nearest neighbor search of design layouts.

DEBUG MODE

External dependencies, to be installed e.g. via pip:
- gurobi v8.1.1

Author: Luis A. Leiva <luis.leiva@aalto.fi>
'''

from __future__ import division, print_function

import knn
from mock import patch

def my_layout_distance(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

@patch('knn.layout_distance', side_effect=my_layout_distance)
def foo(self):
    points = [(0,0), (1,1), (10,10)]
    query = (5,5)
    print('Dataset:', points)
    print('Query:', query)
    print('Closest:', knn.nearest_neighbors(query, points))
    print('Creative:', knn.creative_neighbors(query, points))

if __name__ == '__main__':
    foo()
