from read_table import read_table
from common import common_argparser

parser = common_argparser()
parser.add_argument('table', nargs='?', default=None)
parser.add_argument('--freq-table', nargs='?', default=None)
args = parser.parse_args()

table = ((text, code) for text, code in
         read_table(args.table, args.delimiter))

if args.freq_table:
    text_freq = {text: float(freq) for text, freq in
        read_table(args.freq_table, args.delimiter)}
    min_freq = 0
else:
    text_freq = dict()
    min_freq = 1

code_freq = dict()
for text, code in table:
    for c in code:
        if c in code_freq:
            code_freq[c] += text_freq.get(text, min_freq)
        else:
            code_freq[c] = text_freq.get(text, min_freq)

ranking = [(freq, code) for code, freq in code_freq.items()]
ranking.sort(reverse=True)

for freq, code in ranking:
    print(f'{code}\t{freq}')
