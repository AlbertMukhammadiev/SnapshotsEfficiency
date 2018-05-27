def cow(source, snapshot):
    return 2 * sum(source * snapshot)


def row(snapshots):
    if (len(snapshots) == snapshots.maxlen):
        removed = snapshots.popleft()
        last = snapshots.popleft()
        migratory = (last != removed) * removed
        snapshots.appendleft(last + migratory)
        snapshots.appendleft(removed != migratory)
        return sum(migratory)
    else:
        return 0

def row_m(snapshots):
    if (len(snapshots) == snapshots.maxlen):
        removed = snapshots.popleft()
        migr = removed.copy()
        current = snapshots.popleft()
        while sum(migr):
            next_snap = snapshots.popleft()
            print(migr)
            migr = (current != migr) * migr
            print(migr, '\n')
            next_migr = (next_snap != migr) * migr
            current += (migr != next_migr)
            snapshots.append(current)
            current = next_snap
            migr = next_migr
        snapshots.append(current)
        snapshots.appendleft(removed)

def row_m1(snapshots):
    if (len(snapshots) == snapshots.maxlen):
        removed = snapshots.popleft()
        current = snapshots.popleft()
        migr = (current != removed) * removed
        rest = (removed != migr)
        while sum(migr):
            next_snap = snapshots.popleft()
            next_migr = (next_snap != migr) * migr
            current += (migr != next_migr)
            snapshots.append(current)
            current = next_snap
            migr = next_migr
        snapshots.append(current)
        snapshots.appendleft(rest)
        return sum(removed) - sum(rest)
    else:
        return 0

from collections import deque
from numpy import array

if __name__ == '__main__':
    # arr0 = array([1,0,0,0,1,1,0,0,0,0,1,1]).astype(bool)
    # arr1 = array([0,0,1,0,1,0,0,1,0,1,0,0]).astype(bool)
    # arr2 = array([1,0,0,1,0,0,0,0,1,0,0,0]).astype(bool)
    # arr3 = array([0,1,0,0,0,0,1,0,0,0,1,0]).astype(bool)
    # arr4 = array([1,0,0,0,0,1,0,0,0,0,0,1]).astype(bool)
    arr0 = array([1,0,0,0,1,1,0,0,0,0,1,1])
    arr1 = array([0,0,1,0,1,0,0,1,0,1,0,0])
    arr2 = array([1,0,0,1,0,0,0,0,1,0,0,0])
    arr3 = array([0,1,0,0,0,0,1,0,0,0,1,0])
    arr4 = array([1,0,0,0,0,1,0,0,0,0,0,1])
    xs = deque([arr0, arr1, arr2, arr3, arr4], maxlen=5)
    def print_snaps(snaps):
        for snap in snaps:
            for cell in snap:
                print('*|', end='') if cell else print(' |', end='')
            print()
        print()

    print_snaps(xs)
    print(row_m1(xs))
    print_snaps(xs)