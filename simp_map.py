import re

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

    if args.table:
        with open(args.table, encoding='utf-8') as f:
            simp_map = ((text, simp_code(code, method)) for text, code in (
                line.split('\t') for line in f.read().splitlines()
            ))
    else:
        simp_map = ((text, simp_code(code, method)) for text, code in
            csv.reader((line.strip() for line in sys.stdin),
                delimiter='\t')
        )

    for text, code in simp_map:
        print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
