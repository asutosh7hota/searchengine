#!/usr/bin/env python3
# coding: utf-8

'''
Nearest neighbor search of design layouts.

External dependencies, to be installed e.g. via pip:
- gurobi v8.1.1

NB: Niraj's solver works with python3 only.

Author: Luis A. Leiva <luis.leiva@aalto.fi>
'''

import sys
import os

# --- BEGIN Niraj's lib ---
# Add Niraj to $PYTHONPATH so that we don't have to instrument each submodule.
sys.path.append(os.path.join(os.path.dirname(__file__), 'LayoutCompare'))
from tools.JSONLoader import loadJSONFile
from solver.PrepareParameters import prepare
from solver.MIPCompare import solve
from model import Layout
# --- END Niraj's lib ---


def layout_distance(a, b):
    '''
    Compute difference between 2 layouts.
    '''
    if type(a) is not Layout or type(b) is not Layout:
        raise ValueError('Please use loadJSONFile to read layout files.')
    print('Computing layout distance from {} to {} ...'.format(a.id, b.id), file=sys.stderr)
    prepare(a, b)
    return solve(a, b)


def distance_tuples(query_pt, candidates):
    '''
    Convenient list of <index, distance> tuples to ease neighbor search.
    '''
    return [(index, layout_distance(query_pt, candidate_pt)) for index, candidate_pt in enumerate(candidates)]


def select_neighbors(candidates, distance_tuples, num_results):
    '''
    Pick the actual neighbors according to given distance tuples.
    '''
    indices = [tup[0] for tup in distance_tuples]
    sel_indices = indices[0:num_results]
    return [candidates[i] for i in sel_indices]


def nearest_neighbors(query_pt, candidates, num_results=1):
    '''
    Retrieve the closest neighbors from a pool of candidates
    according to given query object.
    '''
    distances = distance_tuples(query_pt, candidates)
    print('Candidate distances:', distances, file=sys.stderr)
    sort_distances = sorted(distances, key=lambda x: x[1], reverse=False)
    return select_neighbors(candidates, sort_distances, num_results)


def creative_neighbors(query_pt, candidates, num_results=1):
    '''
    Retrieve the "creative" neighbors from a pool of candidates
    according to given query object.
    '''
    distances = distance_tuples(query_pt, candidates)
    sort_distances = sorted(distances, key=lambda x: x[1], reverse=False)
    num_candidates = len(candidates)
    max_candidates = num_results * 10
    if num_candidates > max_candidates:
        max_candidates = num_candidates
    nearest_distances = sort_distances[0:max_candidates]
    sort_nearest = sorted(nearest_distances, key=lambda x: x[1], reverse=True)
    return select_neighbors(candidates, sort_nearest, num_results)


if __name__ == '__main__':
    # Usage example.
    a_file, b_file = sys.argv[1:3]
    print('Layout file 1:', a_file)
    print('Layout file 2:', b_file)
    a = loadJSONFile(a_file)
    b = loadJSONFile(b_file)
#    from tools.JSONDisplay import actualDisplay
#    actualDisplay(a, a_file)
#    actualDisplay(b, b_file)
    print(layout_distance(a, b))
