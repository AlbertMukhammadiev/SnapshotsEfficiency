from sys import argv
from argparse import ArgumentParser, ArgumentTypeError
from numpy import zeros, hstack, random
from csv import writer

import distribute


def dimensions(string):
    """Verify whether given string is a tuple of dimensions"""
    try:
        dim = tuple(int(x) for x in string.split(','))
    except ValueError as ve:
        raise ArgumentTypeError(str(ve))

    if not len(dim) == 3:
        raise ArgumentTypeError(
            'dimensions should be three, e.g. \'1024,64,4\''
        )

    volume_size, block_size, subblock_size = dim
    if volume_size % block_size or block_size % subblock_size:
        raise ArgumentTypeError('incorrect dimensions')
    
    return dim


def percentage(string):
    """Verify whether given string is a percantage"""
    try:
        value = float(string)
    except ValueError as ve:
        raise ArgumentTypeError(str(ve))
    
    if not 0 < value < 100:
        raise ArgumentTypeError('{0} is not a percentage'.format(string))

    return value


def create_parser():
    """Parse command-line arguments and return parser."""
    parser = ArgumentParser(
        description='Create data distribution model. '\
                    'This model iteratively imitates the distribution of data coming in between the snapshots. '\
                    'After each iteration the model generates string that correspond to one block '\
                    'and this string is written to csv file.\nFormat of string in csv: N,n,0,1,1,0,...., '\
                    'where N - number of snapshot, n - number of block, and sequence of 0 and 1 is responsable for the presence of the writing.'
    )
    parser.add_argument('dim', type=dimensions,
                        help='overall dimensions in the form \'vs, bs, ss\', '\
                        'where vs, bs, ss are size of volume, block, '\
                        'subblock accordingly, bytes.')
    parser.add_argument('f', type=str,
                        help='name of csv file(without extension)')
    parser.add_argument('n', type=int,
                        help='number of iterations')
    parser.add_argument('diff', type=int,
                        help='size of data coming in between the snapshots, bytes')
    parser.add_argument('over', type=percentage,
                        help='percentage of data is being overwritten, %%')

    distribution = parser.add_mutually_exclusive_group(required=True)
    distribution.add_argument('--normal', action='store_true',
                              help='choose normal distribution of data')
    distribution.add_argument('--uniform', action="store_true",
                              help='choose uniform distribution of data')
    distribution.add_argument('--sequential', action="store_true",
                              help='choose sequential distribution of data')
    return parser


def commit_changes(snapshot, dimensions, file_name, acc=[0]):
    """Log the data that came after snapshot to csv flie.

    Structure: snapshot number, block number, sequence of {0,1},
    where 1 means that cell is occupied, 0 - free
    """
    volume_size, block_size, subblock_size = dimensions
    with open('tests/{0}.csv'.format(file_name), 'a', newline='') as fout:
        csv_writer = writer(fout)
        snapshot.shape = volume_size // block_size, block_size // subblock_size
        for i, block in enumerate(snapshot):
            csv_writer.writerow(hstack((acc[0], i, block.astype(int))))

    acc[0] += 1


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(argv[1:])
    
    volume_size, block_size, subblock_size = args.dim
    ncells = volume_size // subblock_size
    nwrite = args.diff // subblock_size
    logical_space = zeros(ncells, dtype=bool)
    
    if args.uniform:
        for _ in range(args.n):
            snapshot = logical_space.copy()
            distribute.uniform_ow(snapshot, nwrite, int(nwrite * args.over / 100))
            logical_space += snapshot
            commit_changes(snapshot, args.dim, args.f)
            if logical_space.size - sum(logical_space) < nwrite:
                print('there is no free space on volume(logical)')
                break
    elif args.sequential:
        for _ in range(args.n):
            snapshot = zeros(ncells, dtype=bool)
            distribute.sequential(snapshot, random.randint(ncells), nwrite)
            logical_space += snapshot
            commit_changes(snapshot, args.dim, args.f)
            if logical_space.size - sum(logical_space) < nwrite:
                print('there is no free space on volume(logical)')
                break
    elif args.normal:
        for _ in range(args.n):
            snapshot = zeros(ncells, dtype=bool)
            distribute.normal(snapshot, nwrite)
            logical_space += snapshot
            commit_changes(snapshot, args.dim, args.f)
            if logical_space.size - sum(logical_space) < nwrite:
                print('there is no free space on volume(logical)')
                break