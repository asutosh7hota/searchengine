#!/usr/bin/env python3
# coding: utf-8

'''
Create distance matrix for a pool of layout files.

External dependencies, to be installed e.g. via pip:
- gurobi v8.1.1

NB: Niraj's solver works with python3 only.

Author: Luis A. Leiva <luis.leiva@aalto.fi>
'''

import sys
import os
import re
import glob
from collections import defaultdict
from knn import layout_distance
from tools.JSONLoader import loadJSONFile

if __name__ == '__main__':
    layout_files = sys.argv[1:]
    for l in layout_files:
        if '*' in l:
            layout_files = glob.glob(layout_files.pop())
            break

    print('Processing {} files ...'.format(len(layout_files)), file=sys.stderr)

    layout_cache = {}    
    def get_layout(filename):
        if filename not in layout_cache:
            layout_cache[filename] = loadJSONFile(filename)
        return layout_cache[filename]

    # Generate simple & clean column names.
    def colname(n):
        source = os.path.basename(n)
        source = os.path.splitext(source)[0]
        return re.sub('\W+', '', source)

    matrix = defaultdict(lambda: defaultdict(list))
  
    columns = []
    header_printed = False
    for query_layout_file in layout_files:
        current_row = []
        query_layout = get_layout(query_layout_file)
        columns.append(query_layout_file)
        for other_layout_file in layout_files:
            other_layout = get_layout(other_layout_file)
            # Skip trivial computations, to save time.
            if query_layout_file == other_layout_file:
                # Distance to the same element.
                matrix[query_layout_file][other_layout_file] = 0.0
            if other_layout_file in matrix and query_layout_file in matrix[other_layout_file]:
                # Distance already computed, so leverage the symmetry property.
                matrix[query_layout_file][other_layout_file] = matrix[other_layout_file][query_layout_file]
            else:
                # Compute distance.
                matrix[query_layout_file][other_layout_file] = layout_distance(query_layout, other_layout)
            # Store row computations.
            current_row.append(matrix[query_layout_file][other_layout_file])
            if not header_printed:
                columns.append(other_layout_file)

        # A row is done, so save results.
        linsep = '\t'
        if not header_printed:
            header = [colname(col) for col in columns]
            print(linsep.join(header))
            header_printed = True

        print(linsep.join(map(str, current_row)))
