from read_table import *
from common import common_argparser

parser = common_argparser()
parser.add_argument('table1')
parser.add_argument('table2', nargs='?')
parser.add_argument('-d', '--difference', action='store_true')
parser.add_argument('-sd', '--sym-diff', action='store_true')
parser.add_argument('-st', '--second-table', action='store_true')
args = parser.parse_args()

table1 = read_table(args.table1, args.delimiter)
table2 = read_table(args.table2, args.delimiter)

set1 = set(row[0] for row in table1)
set2 = set(row[0] for row in table2)

delim = args.delimiter if args.delimiter else DEFAULT_DELIM

if args.sym_diff:
    diff1 = set1.difference(set2)
    diff2 = set2.difference(set1)
    for row in table1:
        if row[0] in diff1:
            print(delim.join(row))

    print()

    for row in table2:
        if row[0] in diff2:
            print(delim.join(row))

    exit()

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
        print(delim.join(row))
