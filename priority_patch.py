def main() -> None:
    from read_table import read_table
    from common import common_argparser

    parser = common_argparser()
    parser.add_argument('ptable1')
    parser.add_argument('ptable2')
    parser.add_argument('-c', '--char-only', action='store_true')
    args = parser.parse_args()

    if args.char_only:
        ptable1 = {frozenset(chars):chars for chars, *_ in
            read_table(args.ptable1, args.delimiter)}
        ptable2 = {frozenset(chars):chars for chars, *_ in
            read_table(args.ptable2, args.delimiter)}
    else:
        ptable1 = {frozenset(texts):','.join(texts) for texts in
            read_table(args.ptable1, args.delimiter)}
        ptable2 = {frozenset(texts):','.join(texts) for texts in
            read_table(args.ptable2, args.delimiter)}

    ptable1.update(ptable2)

    for priority in ptable1.values():
        print(priority)

if __name__ == '__main__':
    main()
