import sys, csv, argparse
from read_table import *
from common import common_argparser

parser = common_argparser()
parser.add_argument('tables', nargs='+')
parser.add_argument('-si', '--stdin', action='store_true')
args = parser.parse_args()

mb = dict()
if args.stdin:
    mb = {text:code for text, code in
        read_table(args.delimiter)}

for file in args.tables:
    mb.update({text:code for text, code in
        read_table(file, args.delimiter)})

for text, code in mb.items():
    print(f'{text}\t{code}')
