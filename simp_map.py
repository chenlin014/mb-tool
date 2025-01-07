import re
from read_table import *

def simp_code(code, method):
    if len(code) <= len(method):
        return code
    return ''.join(code[ind] for ind in method)

def main():
    from common import common_argparser

    parser = common_argparser()
    parser.add_argument('method', help='取码法')
    parser.add_argument('table', help='码表', nargs='?', default=None)
    args = parser.parse_args()

    method = tuple(int(i) for i in args.method.split(','))

    simp_map = ((text, simp_code(code, method)) for text, code in
        read_table(args.table, args.delimiter))

    for text, code in simp_map:
        print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
