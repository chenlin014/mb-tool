import re
from read_table import *

def simple_transform(table, old2new):
    for text, code in table:
        yield (text, ''.join(old2new[c] for c in code))

def transform_w_rule(table, old2new, rules):
    for text, code in table:
        for pattern, indexes in rules:
            if not re.match(pattern, code):
                continue

            ncode = ''
            for ind1, ind2 in indexes:
                try:
                    ncode += old2new[code[ind1]][ind2]
                except:
                    continue

            yield (text, ncode)
            break;

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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('old2new', help='旧码对新码')
    parser.add_argument('table', nargs='?', help='码表', default=None)
    parser.add_argument('-r', '--rule_table', help='取码规则文件', default=None)
    args = parser.parse_args()

    old2new = {old:new for old, new in
        table_from_file(args.old2new)}

    table = from_file_or_stdin(args.table)

    if not args.rule_table:
        for text, code in simple_transform(table, old2new):
            print(f'{text}\t{code}')
        quit()

    rules = [(pattern, parseMethod(method)) for pattern, method in
        table_from_file(args.rule_table)]

    for text, code in transform_w_rule(table, old2new, rules):
        print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
