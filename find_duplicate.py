def find_dup_code(table):
    dup_code = dict()
    reverse_table = dict()

    for text, code in table:
        if not code in reverse_table:
            reverse_table[code] = text
            continue

        if code in dup_code:
            dup_code[code].append(text)
        else:
            dup_code[code] = [reverse_table[code], text]

    return dup_code

from read_table import *

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('-pt', '--priority_table', default=None,
        help='排序表：用于排序重码的字')
    parser.add_argument('-r', '--reverse', action='store_true')
    args = parser.parse_args()

    mb = from_file_or_stdin(args.table)

    if args.reverse:
        mb = [(code, text) for text, code in mb]

    if args.priority_table:
        priority_table = {code:texts for
            code, texts in table_from_file(args.priority_table)}
    else:
        priority_table = dict()

    dup_code = find_dup_code(mb)
    dup_code = {code: [text for text in texts if not text in priority_table.get(code, '')]
        for code, texts in dup_code.items()}
    dup_code = {code: texts for code, texts in dup_code.items() if len(texts) > 1}

    print(f'重码率：{sum(len(texts) for texts in dup_code.values())}/{len(mb)}')
    for code, texts in dup_code.items():
        print(f'{code}\t{",".join(texts)}')

if __name__ == "__main__":
    main()
