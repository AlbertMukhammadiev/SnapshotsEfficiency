from sys import argv
from argparse import ArgumentParser
from csv import reader
from numpy import array
from collections import deque

import migrations


def create_parser():
    """Parse command-line arguments and return parser."""
    parser = ArgumentParser(
        description='Compute the efficiency of using snapshots for the '\
                    'selected algorithm and the number of active snapshots. '\
                    'Efficiency is the amount of data migrating and '\
                    'the ratio of occupied logical blocks to physical ones.'
    )
    
    parser.add_argument('filename', type=str,
                        help='name of csv file (without extension) '\
                             'that represents the data distribution model')
    parser.add_argument('nactive', type=int,
                            help='number of active snapshots')

    algorithm = parser.add_mutually_exclusive_group(required=True)
    algorithm.add_argument('--cow', action='store_true',
                              help='choose copy-on-write algorithm')
    algorithm.add_argument('--row', action="store_true",
                              help='choose redirect-on-write algorithm')
    algorithm.add_argument('--row_m', action="store_true",
                              help='choose redirect-on-write algorithm '\
                                   'with forward refs')
    return parser


def row_efficiency(file_name, nactive, modified=False):
    """Compute and return the number of migrating data for row.
    
    Arguments:
    file_name -- name of csv file (with extension)
    nactive -- number of active snapshots
    """
    migrations_row = migrations.row_m if modified else migrations.row
    migrations_count = 0
    source = dict()
    snapshots = dict()
    with open(file_name, newline='') as fin:
        block_reader = reader(fin)
        for line in block_reader:
            values = array(line, dtype=int)
            isnap, iblock, block = values[0], values[1], values[2:].astype(bool)
            try: 
                migrations_count += migrations_row(snapshots[iblock])
                source[iblock] += block
                snapshots[iblock].append(block)
            except KeyError:
                source[iblock] = block.copy()
                snapshots[iblock] = deque([block], maxlen=nactive)

    return migrations_count        


def cow_efficiency(file_name, nactive):
    """Compute and return the number of migrating data for cow.
    
    Arguments:
    file_name -- name of csv file (with extension)
    nactive -- number of active snapshots
    """
    migrations_count = 0
    source = dict()
    snapshots = dict()
    with open(file_name, newline='') as fin:
        block_reader = reader(fin)
        for line in block_reader:
            print(line)
            values = array(line, dtype=int)
            isnap, iblock, block = values[0], values[1], values[2:].astype(bool)
            try:
                migrations_count += migrations.cow(source[iblock], block)
                source[iblock] += block
                snapshots[iblock].append(block)
            except KeyError:
                source[iblock] = block
                snapshots[iblock] = deque(block, maxlen=nactive)

    return migrations_count


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(argv[1:])
    migrations = 0

    if args.cow:
        migrations = cow_efficiency(args.filename + '.csv', args.nactive)
    elif args.row:
        migrations = row_efficiency(args.filename + '.csv', args.nactive)
    elif args.row_m:
        migrations = row_efficiency(args.filename + '.csv', args.nactive, True)
    
    print(migrations)