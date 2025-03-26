import json, re
from read_table import *
from common import common_argparser

ACT_TO_ROWS = {
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

def acts_to_keys(actions, system, act2rows=ACT_TO_ROWS, onLeft=True):
    if actions.startswith('<'):
        actions = actions[1:]
        onLeft = True
    if actions.startswith('>'):
        actions = actions[1:]
        onLeft = False

    if onLeft:
        keys = set(''.join(''.join(system[row][col] for row in act2rows[act])
            for col, act in enumerate(actions) if act in act2rows))
    else:
        last_col = len(system['0']) - 1 if '0' in system else system['row_len'] - 1
        last_col = system['row_len'] - 1 if 'row_len' in system else len(system['0']) - 1
        keys = set(''.join(''.join(system[row][last_col-col] for row in act2rows[act])
            for col, act in enumerate(actions) if act in act2rows))

    for act in actions:
        if act in act2rows:
            continue

        if act in act2rows['tk']:
            if onLeft:
                keys = keys | set(''.join(system['thumb_keys'][col] for col in act2rows['tk'][act]))
            else:
                keys = keys | set(''.join(system['thumb_keys'][len(system['thumb_keys'])-1-col] for col in act2rows['tk'][act]))
        elif act in system['key_order']:
            keys.add(act)

    return keys

def keys_to_chord(keys, order):
    chord = list(keys)
    chord.sort(key=lambda k: order[k])
    return ''.join(chord)

def acts_to_chord(actions, system, act2rows=ACT_TO_ROWS, onLeft=True):
    keys_to_chord(
        acts_to_keys(actions, system, act2rows, onLeft)
    )

def main():
    parser = common_argparser()
    parser.add_argument('system', help='并击系统')
    parser.add_argument('chordmap', help='字根并击表')
    parser.add_argument('table', nargs='?', help='码表', default=None)
    args = parser.parse_args()

    with open(args.system) as f:
        system = json.loads(f.read())
    system['key_order'] = {key: i for i, key in enumerate(system['key_order'])}

    code2keys = {code:(acts_to_keys(acts, system, onLeft=True),
                     acts_to_keys(acts, system, onLeft=False)) for code, acts in
                    read_table(args.chordmap, delimiter=args.delimiter)}

    table = read_table(args.table, args.delimiter)

    for text, codes in table:
        if re.match(r'\{.+\}', codes):
            chords = [apply_keymap(chord, system, onLeft=(i%2 == 0)) for i, chord in
                enumerate(codes[1:-1].split(','))]
            codes = ''
        else:
            chords = []

        for i, part in enumerate(codes.split(' ')):
            keys = set()
            for code in part:
                keys = keys | code2keys[code][i%2]

            chord = keys_to_chord(keys, system['key_order'])
            chords.append(''.join(chord))

        strokes = [(lchord, rchord) for lchord, rchord in zip(chords[::2], chords[1::2])]

        if len(chords) % 2 == 1:
            strokes.append((chords[-1],))

        print(f'{text}\t{" | ".join("<>".join(stroke) for stroke in strokes)}')

if __name__ == '__main__':
    main()
