from read_table import *
import json

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('codemap', help='单指码布局')
    parser.add_argument('keymap', help='键盘布局')
    parser.add_argument('table', nargs='?', help='码表', default=None)
    args = parser.parse_args()

    with open(args.codemap) as f:
        codemap = json.load(f)
    with open(args.keymap) as f:
        keymap = json.load(f)
    key4code = {code: key for code, key in zip(codemap, keymap)}

    for text, code in from_file_or_stdin(args.table):
        print(f'{text}\t{"".join(key4code[c] for c in code)}')

if __name__ == '__main__':
    main()
