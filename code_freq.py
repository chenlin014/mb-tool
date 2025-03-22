from read_table import read_table
from common import common_argparser

parser = common_argparser()
parser.add_argument('table', nargs='?', default=None)
parser.add_argument('--freq-table', nargs='?', default=None)

table = ((text, code) for text, code in
         read_table(args.table, args.delimiter))

if args.freq_table:
    text_freq = {text: float(freq) for text, freq in
        read_table(args.freq_table, args.delimiter)}

with open(sys.argv[1], encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    mb = {zi:ma for zi, ma in reader}
code_freq = {code:0 for code in set(''.join(mb.values()))}

if len(sys.argv) <= 2:
    for code in ''.join(mb.values()):
        code_freq[code] += 1
else:
    with open(sys.argv[2], encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        char_freq = [(char, float(freq)) for char, freq in reader]
    for char, freq in char_freq:
        if not char in mb:
            continue

        for code in mb[char]:
            code_freq[code] += freq

ranking = [(freq, code) for code, freq in code_freq.items()]
ranking.sort(reverse=True)

for freq, code in ranking:
    print(f'{code}\t{freq}')
