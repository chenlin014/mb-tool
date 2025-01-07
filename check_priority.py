def main() -> None:
    from read_table import read_table
    from common import common_argparser
    from find_duplicate import find_dup_code

    parser = common_argparser()
    parser.add_argument('priority_table')
    parser.add_argument('code_table')
    args = parser.parse_args()

    ptable = {code: chars for code, chars in
        read_table(args.priority_table, args.delimiter)}

    mb = [(text, code) for text, code in
        read_table(args.code_table, args.delimiter)]

    dup_code = find_dup_code(mb)

    missingTable = dict()
    extraTable = dict()
    for code, texts in dup_code.items():
        texts = set(texts)
        if not code in ptable:
            missingTable[code] = texts
            continue

        ptexts = set(ptable[code])
        missing = texts.difference(ptexts)
        if missing:
            missingTable[code] = missing

    for code, ptexts in ptable.items():
        ptexts = set(ptexts)
        if not code in dup_code:
            extraTable[code] = set(ptexts)
            continue

        texts = set(dup_code[code])
        extra = ptexts.difference(texts)
        if extra:
            extraTable[code] = extra

    if missingTable:
        print('缺少：')
        for code, texts in missingTable.items():
            missing = ','.join(texts)
            if code in ptable:
                missing = f'({missing})'
            print(f'{code}\t{missing}')
        print()
    if extraTable:
        print('多余：')
        for code, texts in extraTable.items():
            extra = ','.join(texts)
            print(f'{code}\t{extra}')

if __name__ == '__main__':
    main()
