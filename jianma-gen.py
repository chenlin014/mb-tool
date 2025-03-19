def gen_jianma(code, method):
    try:
        return ''.join(code[ind] for ind in method)
    except:
        return None

def gen_jianma_table(mb, methods, char_freq=dict()):
    mt_num = {text: 0 for text in mb}
    mt_cnt = len(methods)
    jm_table = {text: gen_jianma(code, methods[0]) for text, code in
        mb.items()}

    min_lens = []
    for method in methods:
        min_lens.append(
            max(i + 1 if i >= 0 else i * -1 for i in method)
        )

    has_problem = True
    while has_problem:
        has_problem = False
        reverse_table = dict()
        need_update = set()
        conflicts = dict()

        for text, jm in jm_table.items():
            if mt_num[text] >= mt_cnt:
                continue
            if not jm:
                has_problem = True
                need_update.add(text)
                continue

            if jm in reverse_table:
                has_problem = True
                if jm in conflicts:
                    conflicts[jm].append(text)
                else:
                    conflicts[jm] = [reverse_table[jm], text]
            else:
                reverse_table[jm] = text

        for jm, texts in conflicts.items():
            most_frequent = texts[0]
            for text in texts[1:]:
                if char_freq.get(text, 0) > char_freq.get(most_frequent, 0):
                    most_frequent = text

            for text in texts:
                if text != most_frequent:
                    need_update.add(text)

        for text in need_update:
            mt_num[text] += 1
            if mt_num[text] >= mt_cnt:
                jm_table[text] = None
            else:
                jm_table[text] = gen_jianma(mb[text], methods[mt_num[text]])

    return {text: jm for text, jm in
        jm_table.items() if jm and mt_num[text] < mt_cnt}

def main() -> None:
    from read_table import read_table
    from common import common_argparser
    parser = common_argparser()
    parser.add_argument('methods')
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('--char-freq', nargs='?', default=None)
    args = parser.parse_args()

    methods = tuple(
                    tuple(map(int, method.split(',')))
                for method in args.methods.split(':'))

    mb = {text:code for text, code in
        read_table(args.table, args.delimiter)}

    if args.char_freq:
        char_freq = {char: float(freq) for char, freq in
            read_table(args.char_freq, args.delimiter)}
    else:
        char_freq = dict()

    jm_table = gen_jianma_table(mb, methods, char_freq)

    for text, jm in jm_table.items():
        print(f'{text}\t{jm}')

if __name__ == '__main__':
    main()
