import json, csv, argparse, re
from common import *

ACTIONS = {
    '0': (),
    '1': ('+1',),
    '2': ('0',),
    '3': ('+1', '0'),
    '4': ('-1',),
    '5': ('0', '-1'),
    'tk': {
        'a': (0,),
        'b': (1,),
        'c': (0, 1),
        'd': (2,),
        'e': (1, 2)
    }
}

def apply_keymap(code, system, acts=ACTIONS, onLeft=True):
    if code.startswith('<'):
        code = code[1:]
        onLeft = True
    if code.startswith('>'):
        code = code[1:]
        onLeft = False

    if onLeft:
        keys = set(''.join(''.join(system[row][col] for row in acts[act])
            for col, act in enumerate(code) if act in acts))
    else:
        last_col = len(system['0']) - 1 if '0' in system else system['row_len'] - 1
        last_col = system['row_len'] - 1 if 'row_len' in system else len(system['0']) - 1
        keys = set(''.join(''.join(system[row][last_col-col] for row in acts[act])
            for col, act in enumerate(code) if act in acts))

    for act in code:
        if act in acts:
            continue

        if act in acts['tk']:
            if onLeft:
                keys = keys | set(''.join(system['thumb_keys'][col] for col in acts['tk'][act]))
            else:
                keys = keys | set(''.join(system['thumb_keys'][len(system['thumb_keys'])-1-col] for col in acts['tk'][act]))
        elif act in system['key_order']:
            keys.add(act)

    chord = list(keys)
    chord.sort(key=lambda k: system['key_order'][k])
    return ''.join(chord)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('system', help='并击系统')
    parser.add_argument('chordmap', help='字根并击表')
    parser.add_argument('mb_path', nargs='?', help='码表', default=None)
    args = parser.parse_args()

    with open(args.system) as f:
        system = json.loads(f.read())
    system['key_order'] = {key: i for i, key in enumerate(system['key_order'])}

    chord_map = {code:(apply_keymap(chord, system, onLeft=True),
                     apply_keymap(chord, system, onLeft=False)) for code, chord in
                    table_from_file(args.chordmap, delimiter='\t')}

    mb = from_file_or_stdin(args.mb_path)

    for zi, ma in mb:
        if re.match(r'\{.+\}', ma):
            chords = [apply_keymap(chord, system, onLeft=(i%2 == 0)) for i, chord in
                enumerate(ma[1:-1].split(','))]
            ma = ''
        else:
            chords = []

        for i, code in enumerate(ma.split(' ')):
            keys = set()
            for c in code:
                keys = keys | set(chord_map[c][i%2])

            chord = list(keys)
            chord.sort(key=lambda k: system['key_order'][k])
            chords.append(''.join(chord))

        strokes = [(lchord, rchord) for lchord, rchord in zip(chords[::2], chords[1::2])]

        if len(chords) % 2 == 1:
            strokes.append((chords[-1],))

        print(f'{zi}\t{" | ".join("<>".join(stroke) for stroke in strokes)}')

if __name__ == '__main__':
    main()
