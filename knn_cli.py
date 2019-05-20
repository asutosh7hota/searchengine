#!/usr/bin/env python3
# coding: utf-8

'''
Nearest neighbor search of design layouts.

NB: This program works with python3 only.

Author: Luis A. Leiva <luis.leiva@aalto.fi>
'''

import sys
import os
import json
import argparse

import knn
# Add Niraj to $PYTHONPATH so that we don't have to instrument each submodule.
sys.path.append(os.path.join(os.path.dirname(__file__), 'LayoutCompare'))
from tools.JSONLoader import loadJSONFile

parser = argparse.ArgumentParser()
parser.add_argument('--query', help='query layout file')
parser.add_argument('--querydir', help='path to a directory with query layout files')
parser.add_argument('--candidates', nargs='+', help='candidate layout files')
parser.add_argument('--candidatesdir', help='path to a directory with candidate layout files')
parser.add_argument('--distance', nargs='+', help='two layout files to compare their distance')
args = parser.parse_args()

if args.distance:
    # Bonus usage of this CLI: The --distance arg allows to compare two layouts,
    # so we'll exit the program when completed.
    a, b = [loadJSONFile(f) for f in args.distance[0:2]]
    print('Distance:', knn.layout_distance(a, b))
    exit()


def get_json_files(files):
    res = []
    for filename in files:
        if os.path.splitext(filename)[-1] == '.json':
            res.append(filename)
    return res

def get_json_files_from_directory(dirname):
    return [get_json_files(files) for root, dirs, files in os.walk(dirname)]

if not args.query and not args.querydir:
    sys.exit('Missing --query or --querydir argument.')

if not args.candidates and not args.candidatesdir:
    sys.exit('Missing --candidates or --candidatesdir argument.')

query_files = [args.query] if args.query is not None else get_json_files_from_directory(args.querydir)
candidate_files = args.candidates if args.candidates is not None else get_json_files_from_directory(args.candidatesdir)

# Ensure there are no duplicates.
query_files = list(set(query_files))
candidate_files = list(set(candidate_files))

for query_file in query_files:
    # Ensure the query file is not in candidates list,
    # for which we create a copy so it doesn't affect the next iteration.
    the_candidate_files = candidate_files[:]
    if query_file in the_candidate_files:
        the_candidate_files.remove(query_file)

    query = loadJSONFile(query_file)
    candidates = [loadJSONFile(f) for f in the_candidate_files]
    # Perform 1-NN search.
    nearest = [candidate.id for candidate in knn.nearest_neighbors(query, candidates, 1)]
    print('Query: {} -- Nearest: {}'.format(query.id, nearest.pop()))
