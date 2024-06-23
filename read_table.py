import sys, csv

def table_from_file(path: str, delimiter='\t', encoding='utf-8'):
    with open(path, encoding=encoding) as f:
        reader = csv.reader((line for line in
            f.read().splitlines() if line.strip() and not line.startswith('#')),
            delimiter=delimiter)
        return [row for row in reader]

def table_from_stdin(delimiter='\t'):
    reader = csv.reader((line.strip() for
        line in sys.stdin if line.strip() and not line.startswith('#')),
        delimiter=delimiter)
    return [row for row in reader]

def from_file_or_stdin(path: str | None):
    if path:
        return table_from_file(path)

    return table_from_stdin()
