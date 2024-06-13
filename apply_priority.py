import csv, argparse
from read_table import *

parser = argparse.ArgumentParser()
parser.add_argument('priority_table')
parser.add_argument('mb_path', nargs='?')
parser.add_argument('-u', '--uniquifier', default=',1,2,3,4,5,6,7,8,9')
args = parser.parse_args()

uniquifier = args.uniquifier.split(',')

with open(args.priority_table, encoding='utf-8') as f:
    update_table = dict()
    for code, chars in csv.reader(f, delimiter='\t'):
        for i, char in enumerate(chars):
            update_table[f'{char}\t{code}'] = code + uniquifier[i]

mb = from_file_or_stdin(args.mb_path)

for text, code in mb:
    if f'{text}\t{code}' in update_table:
        code = update_table[f'{text}\t{code}']

    print(f'{text}\t{code}')
