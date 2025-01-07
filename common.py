import argparse

def common_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--delimiter', default=None)

    return parser
