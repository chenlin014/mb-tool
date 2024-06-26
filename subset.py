import argparse
from read_table import *

parser = argparse.ArgumentParser()
parser.add_argument('table1')
parser.add_argument('table2', nargs='?')
parser.add_argument('-d', '--difference', action='store_true')
args = parser.parse_args()

with open(args.table1, encoding='utf_8') as f:
    table1 = [line.split('\t') for line in
        f.read().splitlines()]

table2 = from_file_or_stdin(args.table2)

set1 = set(line[0] for line in table1)
set2 = set(line[0] for line in table2)
if args.difference:
    subset = set1.difference(set2)
    for line in table1:
        if line[0] in subset:
            print('\t'.join(line))
else:
    subset = set1.intersection(set2)
    for line in table2:
        if line[0] in subset:
            print('\t'.join(line))
