from csv import reader, DictReader
from numpy import array
from collections import deque


def migration_cow(file_name):
    overwrite_count = 0
    total = dict()
    snapshots = dict()
    verifier = dict()
    with open(file_name, newline='') as fin:
        block_reader = reader(fin)
        for row in block_reader:
            values = array(row, dtype=int)
            isnap, iblock, block = values[0], values[1], values[2:].astype(bool)
            
            try:
                verifier[isnap] += 1
            except KeyError:
                verifier[isnap] = 1

            try:
                overwrite_count += sum(total[iblock] * block)
                total[iblock] += block
                snapshots[iblock].append(block)
            except KeyError:
                total[iblock] = block
                snapshots[iblock] = deque(block, maxlen=10)
    
    def check_structure():
        pass
    check_structure()
    print(overwrite_count)

    def check_structure():
        pass
    check_structure()
    print(overwrite_count)

if __name__ == '__main__':
    migration_cow('first.csv')