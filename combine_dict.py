import sys, csv, argparse
from read_table import *

parser = argparse.ArgumentParser()
parser.add_argument('tables', nargs='+')
parser.add_argument('-si', '--stdin', action='store_true')
args = parser.parse_args()

mb = dict()
if args.stdin:
    mb = {text:code for text, code in table_from_stdin()}

for file in args.tables:
    mb.update({text:code for text, code in
        table_from_file(file)})

for text, code in mb.items():
    print(f'{text}\t{code}')
