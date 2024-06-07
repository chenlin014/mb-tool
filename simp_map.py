import re
from common import *

def simp_code(code, method):
    if len(code) <= len(method):
        return code
    return ''.join(code[ind] for ind in method)

def main():
    import sys, argparse, csv

    parser = argparse.ArgumentParser()
    parser.add_argument('method', help='取码法')
    parser.add_argument('table', help='码表', nargs='?', default=None)
    args = parser.parse_args()

    method = tuple(int(i) for i in args.method.split(','))

    simp_map = ((text, simp_code(code, method)) for text, code in
        from_file_or_stdin(args.table))

    for text, code in simp_map:
        print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
