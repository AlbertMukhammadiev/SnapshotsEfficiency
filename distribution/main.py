from sys import argv
from argparse import ArgumentParser, ArgumentTypeError
from numpy import zeros, hstack
from csv import writer

import distribute

def dimensions(string):
    try:
        dim = tuple(int(x) for x in string.split(','))
    except ValueError as ve:
        raise ArgumentTypeError(str(ve))

    if not len(dim) == 3:
        raise ArgumentTypeError(
            'dimensions should consist of three parts, e.g. \'(1024, 64, 4)\''
        )

    volume_size, block_size, subblock_size = dim
    if volume_size % block_size or block_size % subblock_size:
        raise ArgumentTypeError('incorrect dimensions')
    return dim


def percentage(string):
    try:
        value = float(string)
    except ValueError as ve:
        raise ArgumentTypeError(ve)
    
    if not 0 < value < 100:
        message = '{0} is not a percentage'.format(string)
        raise ArgumentTypeError(message)
    
    return value


def create_parser():
    parser = ArgumentParser(description='!_!_TODO_!_!')

    # distribution = parser.add_mutually_exclusive_group(required=True)
    # distribution.add_argument('--normal', action='store_true',
    #                           help='choose normal distribution of data')
    # distribution.add_argument('--uniform', action="store_true",
    #                           help='choose uniform distribution of data')
    # distribution.add_argument('--sequential', action="store_true",
    #                           help='choose sequential distribution of data')

    parser.add_argument('-dim', '--dimensions', type=dimensions,
                        default=(1024, 64, 4), metavar='dim', dest='dimensions',
                        help='overall dimensions in the form \'v, b, s\',\
                        where v - size of volume, b - size of block,\
                        s - size of subblock')
    
    parser.add_argument('-f', '--filename', type=str,
                        default='default.csv', metavar='file name', dest='file_name',
                        help='name of file for store snapshots in csv format')
    
    conditions = parser.add_argument_group('Conditions')
    conditions.add_argument('-n', '--nsnapshots', type=int, default=100,
                            metavar='!_!_TODO_!_!', dest='nsnapshots',
                            help='total number of snapshots')
    conditions.add_argument('-d', '--difference', type=percentage, default=50,
                            metavar='!_!_TODO_!_!', dest='diff_data',
                            help='percentage of data incoming between snapshots, %%')
    conditions.add_argument('-o', '--overwritten', type=percentage, default=50,
                            metavar='!_!_TODO_!_!', dest='overwritten_percentage',
                            help='percentage of data which is written to occupied cells, %%')
    return parser


def commit_changes(snapshot, dimensions, file_name, acc=[0]):
    """Store snapshot state in the file csv format.

    Structure: snapshot number, block number, sequence of {0,1},
    where 1 means that cell is occupied, 0 - free
    """
    volume_size, block_size, subblock_size = dimensions

    # for assessment
    with open('temp.txt', 'a') as fout:
        fout.write(str(acc[0]) + ' ')
        for subblock in snapshot:
            fout.write('*') if subblock else fout.write('_')
        fout.write('\n')

    with open(file_name, 'a') as fout:
        csv_writer = writer(fout)
        snapshot.shape = volume_size // block_size, block_size // subblock_size
        for i, block in enumerate(snapshot):
            csv_writer.writerow(hstack((acc[0], i, block.astype(int))))

    acc[0] += 1


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(argv[1:])
    volume_size, block_size, subblock_size = args.dimensions

    ncells = volume_size // subblock_size
    total = zeros(ncells, dtype=bool)
    nwrite = int(args.diff_data * ncells / 100)
    for i in range(args.nsnapshots):
        snapshot = zeros(ncells, dtype=bool)
        distribute.uniform_ow(snapshot, nwrite, int(nwrite * args.overwritten_percentage / 100))
        commit_changes(snapshot, args.dimensions, args.file_name)