from sys import argv
from argparse import ArgumentParser
from csv import reader, writer
from numpy import array
from collections import deque
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from efficiency import migrations


def create_parser():
    """Parse command-line arguments and return parser."""
    parser = ArgumentParser(
        description='Calculate the efficiency of using snapshots for the '\
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
            isnap, iblock = int(line[0]), int(line[1])
            if not iblock:
                print(isnap)
            block = array(line[2:], dtype=int).astype(bool)
            try:
                migrations_count += migrations_row(snapshots[iblock])
                source[iblock] += block
                snapshots[iblock].append(block)
            except KeyError:
                source[iblock] = block.copy()
                snapshots[iblock] = deque([block], maxlen=nactive)

    logical = 0
    for _, block in source.items():
        logical += bool(sum(block))
    physical = 0
    for _, snapshot in snapshots.items():
        for block in snapshot:
            physical += bool(sum(block))
    return migrations_count, logical / physical


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
            isnap, iblock = int(line[0]), int(line[1])
            if not iblock:
                print(isnap)
            block = array(line[2:], dtype=int).astype(bool)
            try:
                migrations_count += migrations.cow(source[iblock], block)
                source[iblock] += block
                snapshots[iblock].append(block)
            except KeyError:
                source[iblock] = block.copy()
                snapshots[iblock] = deque([block], maxlen=nactive)

    logical = 0
    for _, block in source.items():
        logical += bool(sum(block))
    physical = 0
    for _, snapshot in snapshots.items():
        for block in snapshot:
            physical += bool(sum(block))
    
    return migrations_count, logical / physical


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(argv[1:])
    
    result = (0, 0)
    algorithm = 'None'
    file_name = 'models/' + args.filename + '.csv'
    if args.cow:
        algorithm = 'cow'
        result = cow_efficiency(file_name, args.nactive)
    elif args.row:
        algorithm = 'row'
        result = row_efficiency(file_name, args.nactive)
    elif args.row_m:
        algorithm = 'row_m'
        result = row_efficiency(file_name, args.nactive, True)
    
    with open('models/results.csv', 'a', newline='') as fout:
        csv_writer = writer(fout)
        csv_writer.writerow([args.filename, args.nactive, algorithm, result[0], result[1]])
            
    print(result)