import re
from copy import deepcopy
from read_table import *

def chain_repl(s: str, replmnts: list[str, str], regex: bool=False) -> str:
    if regex:
        replace = lambda pat, repl, s: re.sub(pat, repl, s)
    else:
        replace = lambda pat, repl, s: s.replace(pat, repl)

    ns = s
    for pattern, repl in replmnts:
        ns = replace(pattern, repl, ns)

    return ns

def list_chain_repl(ls: list[str], replmnts: list[str, str], regex: bool=False) -> list[str]:
    return [chain_repl(s, replmnts, regex) for s in ls]

def column_repl(table: list[list[str]], replmnts: list[str, str], column: int = 0, regex: bool=False) -> list[list[str]]:
    new_table = deepcopy(table)

    new_col = list_chain_repl([row[column] for row in table], replmnts, regex)

    for i, value in enumerate(new_col):
        new_table[i][column] = value

    return new_table

def main() -> None:
    from common import common_argparser
    parser = common_argparser()
    parser.add_argument('replmnts')
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-f', '--file', action='store_true')
    parser.add_argument('-re', '--regex', action='store_true')
    args = parser.parse_args()

    if args.file:
        replmnts = read_table(args.replmnts, args.delimiter)
    else:
        replmnts = [repl.split(' -> ', 1) for repl in
            args.replmnts.split('; ')]

    args.column = int(args.column)

    new_table = column_repl(read_table(args.table, args.delimiter),
                            replmnts, args.column, args.regex)
    for row in new_table:
        print('\t'.join(row))

if __name__ == '__main__':
    main()
