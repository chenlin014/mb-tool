import re
from read_table import *

def serial_code(code, key4code, rules):
    for pattern, indexes in rules:
        if not re.search(pattern, code):
            continue

        ncode = ''
        for ind1, ind2 in indexes:
            try:
                ncode += key4code[code[ind1]][ind2]
            except:
                continue

        return ncode

LATIN_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
latin_lower = 'abcdefghijklmnopqrstuvwxyz'

def parseMethod(method: str):
    if not re.match('^([A-Z][a-z])+$', method):
        return None

    output = []
    for upper, lower in zip(method[::2], method[1::2]):
        ind1 = LATIN_UPPER.index(upper)
        ind2 = latin_lower.index(lower)

        if ind1 > 13:
            ind1 = ind1 - 26
        if ind2 > 13:
            ind2 = ind2 - 26

        output.append((ind1, ind2))

    return tuple(output)

def main():
    from common import common_argparser

    parser = common_argparser()
    parser.add_argument('code_key_map', help='码键映射')
    parser.add_argument('table', nargs='?', help='码表', default=None)
    parser.add_argument('-r', '--rule_table', help='取码规则文件', default=None)
    args = parser.parse_args()

    key4code = {code:key for code, key in
        read_table(args.code_key_map, args.delimiter)}

    table = ((text, code) for text, code in
        read_table(args.table, args.delimiter))

    if not args.rule_table:
        for text, code in table:
            keys = ''.join(key4code[c] for c in code)
            print(f'{word}\t{keys}')
        quit()

    rules = [(pattern, parseMethod(method)) for pattern, method in
        read_table(args.rule_table, args.delimiter)]

    for text, code in table:
        ncode = serial_code(code, key4code, rules)
        print(f'{text}\t{ncode}')

if __name__ == '__main__':
    main()
