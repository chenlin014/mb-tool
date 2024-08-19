import re
from copy import deepcopy
from read_table import *

def chain_repl(s: str, replmnts: list[str, str]) -> str:
    ns = s
    for pattern, repl in replmnts:
        ns = re.sub(pattern, repl, ns)

    return ns

def list_chain_repl(ls: list[str], replmnts: list[str, str]) -> list[str]:
    return [chain_repl(s, replmnts) for s in ls]

def column_repl(table: list[list[str]], replmnts: list[str, str], column: int = 0) -> list[list[str]]:
    new_table = deepcopy(table)

    new_col = list_chain_repl([row[column] for row in table], replmnts)

    for i, value in enumerate(new_col):
        new_table[i][column] = value

    return new_table

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('replmnts')
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-f', '--file', action='store_true')
    args = parser.parse_args()

    if args.file:
        replmnts = table_from_file(args.replmnts)
    else:
        replmnts = [repl.split(' -> ', 1) for repl in
            args.replmnts.split('; ')]

    args.column = int(args.column)

    new_table = column_repl(from_file_or_stdin(args.table), replmnts, args.column)
    for row in new_table:
        print('\t'.join(row))

if __name__ == '__main__':
    main()
