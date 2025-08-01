from read_table import *
import json

def main():
    from common import common_argparser
    parser = common_argparser()
    parser.add_argument('codemap', help='区码布局')
    parser.add_argument('keymap', help='键盘布局')
    parser.add_argument('table', nargs='?', help='码表', default=None)
    args = parser.parse_args()

    with open(args.codemap) as f:
        codemap = json.load(f)
    with open(args.keymap) as f:
        keymap = json.load(f)

    for text, codes in read_table(args.table, args.delimiter):
        ncodes = codes
        for code, key in zip(codemap, keymap):
            ncodes = ncodes.replace(code, key)
        print(f'{text}\t{ncodes}')

if __name__ == '__main__':
    main()
