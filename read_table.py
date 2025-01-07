import sys, csv

DEFAULT_DELIM = '\t'

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

def read_table(path=None, delimiter=DEFAULT_DELIM):
    if not delimiter:
        delimiter = DEFAULT_DELIM

    if not path:
        return table_from_stdin(delimiter)

    if path.endswith('.tsv'):
        delim = '\t'
    elif path.endswith('.csv'):
        delim = ','

    return table_from_file(path, delimiter)
