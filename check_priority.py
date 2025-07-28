def main() -> None:
    from read_table import read_table
    from common import common_argparser
    from find_duplicate import find_dup_code

    parser = common_argparser()
    parser.add_argument('priority_table')
    parser.add_argument('code_table')
    parser.add_argument('-c', '--char-only', action='store_true')
    args = parser.parse_args()

    if args.char_only:
        ptable_sets = set(frozenset(texts) for texts, *_ in
            read_table(args.priority_table, args.delimiter))
    else:
        ptable_sets = set(frozenset(texts) for texts in
            read_table(args.priority_table, args.delimiter))

    dup_sets = set(frozenset(texts) for texts in
        find_dup_code(read_table(args.code_table, args.delimiter)).values())

    missing_sets = dup_sets.difference(ptable_sets)
    extra_sets = ptable_sets.difference(dup_sets)

    if args.char_only:
        delim = ''
    elif args.delimiter:
        delim = args.delimiter
    else:
        delim = ','

    if missing_sets:
        print('缺少：')
        for texts in missing_sets:
            print(delim.join(texts))
        print()
    if extra_sets:
        print('多余：')
        for texts in extra_sets:
            print(delim.join(texts))

if __name__ == '__main__':
    main()
