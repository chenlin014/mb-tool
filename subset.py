import argparse
from read_table import *

parser = argparse.ArgumentParser()
parser.add_argument('table1')
parser.add_argument('table2', nargs='?')
parser.add_argument('-d', '--difference', action='store_true')
parser.add_argument('-st', '--second-table', action='store_true')
args = parser.parse_args()

table1 = table_from_file(args.table1)
table2 = from_file_or_stdin(args.table2)

set1 = set(row[0] for row in table1)
set2 = set(row[0] for row in table2)
if args.difference:
    if args.second_table:
        subset = set2.difference(set1)
    else:
        subset = set1.difference(set2)
else:
    subset = set1.intersection(set2)

if args.second_table:
    output = (row for row in table2)
else:
    output = (row for row in table1)

for row in output:
    if row[0] in subset:
        print('\t'.join(row))
