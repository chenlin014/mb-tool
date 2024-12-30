import yaml, re
from read_table import *

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('repl_file')
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('-re', '--regex', action='store_true')
    args = parser.parse_args()

    text2codes = dict()
    for text, code in from_file_or_stdin(args.table):
        if text in text2codes:
            text2codes[text].add(code)
        else:
            text2codes[text] = {code}

    with open(args.repl_file) as f:
        replmnts = yaml.safe_load(f)

    if args.regex:
        replace = lambda pat, repl, s: re.sub(pat, repl, s)
    else:
        replace = lambda pat, repl, s: s.replace(pat, repl)

    texts = set(text2codes)
    for replmnt in replmnts:
        pat = replmnt['pattern']
        repl = replmnt['replacement']
        append = replmnt.get('append', False)

        if 'only' in replmnt:
            for text in replmnt['only']:
                if not text in text2codes:
                    continue

                new_codes = set(replace(pat, repl, code) for code in text2codes[text])
                if append:
                    text2codes[text] |= new_codes
                else:
                    text2codes[text] = new_codes

        excluded = replmnt.get('exclude', set())

        for text in texts:
            if text in excluded:
                continue

            new_codes = set(replace(pat, repl, code) for code in text2codes[text])
            if append:
                text2codes[text] |= new_codes
            else:
                text2codes[text] = new_codes

    for text, codes in text2codes.items():
        for code in codes:
            print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
