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
    args = parser.parse_args()

    mb = from_file_or_stdin(args.table)

    if args.priority_table:
        char_priority = {code:chars for
            code, chars in table_from_file(args.priority_table)}
    else:
        char_priority = dict()

    dup_code = find_dup_code(mb)
    dup_code = {code: [char for char in chars if not char in char_priority.get(code, '')]
        for code, chars in dup_code.items()}
    dup_code = {code: chars for code, chars in dup_code.items() if len(chars) > 1}

    print(f'重码字数：{sum(len("".join(chars)) for chars in dup_code.values())}')
    for code, chars in dup_code.items():
        print(f'{code}\t{",".join(chars)}')

if __name__ == "__main__":
    main()
