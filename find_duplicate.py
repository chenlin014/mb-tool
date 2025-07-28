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
    from common import common_argparser
    parser = common_argparser()
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('-pt', '--priority_table', default=None,
        help='排序表：用于排序重码的字')
    parser.add_argument('-f', '--format', default="{code}\t{texts}",
        help='輸出格式')
    parser.add_argument('-r', '--reverse', action='store_true')
    parser.add_argument('-sr', '--show-rate', action='store_true',
        help='顯示重碼率')
    args = parser.parse_args()

    mb = read_table(args.table, args.delimiter)

    if args.reverse:
        mb = [(code, text) for text, code in mb]

    if args.priority_table:
        priority_table = {code:texts for code, texts in
            read_table(args.priority_table, args.delimiter)}
    else:
        priority_table = dict()

    dup_code = find_dup_code(mb)
    dup_code = {code: [text for text in texts if not text in priority_table.get(code, '')]
        for code, texts in dup_code.items()}
    dup_code = {code: texts for code, texts in dup_code.items() if len(texts) > 0}

    if args.show_rate:
        print(f'重码率：{sum(len(texts) for texts in dup_code.values())}/{len(mb)}')
    for code, texts in dup_code.items():
        if code in priority_table:
            #print(f'{code}\t({",".join(texts)})')
            print(args.format.format(
                code=code, texts=f'({",".join(texts)})'
            ))
        else:
            print(args.format.format(
                code=code, texts=",".join(texts)
            ))
            #print(f'{code}\t{",".join(texts)}')

if __name__ == "__main__":
    main()
