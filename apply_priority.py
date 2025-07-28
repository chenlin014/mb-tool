import csv, argparse
from read_table import *
from common import common_argparser
from find_duplicate import find_dup_code

parser = common_argparser()
parser.add_argument('priority_table')
parser.add_argument('mb_path', nargs='?')
parser.add_argument('-c', '--char-only', action='store_true')
parser.add_argument('-u', '--uniquifier', default=',1,2,3,4,5,6,7,8,9')
args = parser.parse_args()

uniquifier = args.uniquifier.split(',')

with open(args.priority_table, encoding='utf-8') as f:
    if args.char_only:
        reader = (list(chars) for chars in f.read().splitlines())
    else:
        reader = csv.reader(f)
    set2priority = {frozenset(texts):texts for texts in reader}

mb = read_table(args.mb_path, args.delimiter)
dup_code_texts = ((code, frozenset(texts)) for code, texts in
    find_dup_code(mb).items())

code2priority = {code:set2priority[texts] for code, texts in
    dup_code_texts if texts in set2priority}

for text, code in mb:
    if code in code2priority:
        code = f'{code}{uniquifier[code2priority[code].index(text)]}'

    print(f'{text}\t{code}')
