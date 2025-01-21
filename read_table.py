import sys, csv

DEFAULT_DELIM = '\t'
DEFAULT_ENC = 'utf-8'

def table_from_file(path: str, delimiter=DEFAULT_DELIM, encoding='utf-8'):
    with open(path, encoding=encoding) as f:
        reader = csv.reader((line for line in
            f.read().splitlines() if line.strip()),
            delimiter=delimiter)
        return [row for row in reader]

def table_from_stdin(delimiter='\t'):
    reader = csv.reader((line.strip() for
        line in sys.stdin if line.strip()),
        delimiter=delimiter)
    return [row for row in reader]

def read_table(path=None, delimiter=None, encoding='utf-8'):
    if not path:
        if not delimiter:
            delimiter = DEFAULT_DELIM
        return table_from_stdin(delimiter)

    if not delimiter:
        if path.endswith('.tsv'):
            delimiter = '\t'
        elif path.endswith('.csv'):
            delimiter = ','
        else:
            delimiter = DEFAULT_DELIM

    return table_from_file(path, delimiter)
