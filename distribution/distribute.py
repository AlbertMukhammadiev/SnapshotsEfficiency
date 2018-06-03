"""This module contains several functions for distributing data
into array.

Functions:
    sequential(space, startno, ndata) -> None
    uniform(space, ndata) -> None
    uniform_ow(space, ndata, ndata_overwrite) -> None
    normal(space, ndata) -> None
"""

from numpy import arange, hstack, unique, zeros, random


def sequential(space, startno, ndata):
    """Distribute data in space in place sequentially.
    
    Arguments:
    space -- 1-dimensional numpy array that represents space
    startno -- position which the sequential writing begins from
    ndata -- number of cells to write
    """
    space.fill(False)
    remainder = max(0, ndata - (len(space) - startno))
    positions = hstack((arange(remainder), arange(startno, startno + ndata - remainder)))
    space[positions] = True


def uniform(space, ndata):
    """Distribute data in space in place uniformly.
    
    Arguments:
    space -- 1-dimensional numpy array that represents space
    ndata -- total number of cells to write
    """
    space.fill(False)
    if ndata >= len(space):
        space.fill(True)
        return

    positions = zeros(0, dtype=int)
    indices = zeros(0, dtype=int)
    while len(indices) < ndata:
        positions = hstack((positions, random.randint(0, len(space), ndata)))
        _, indices = unique(positions, return_index=True)

    indices.sort()
    space[positions[indices][:ndata]] = True


def uniform_ow(space, ndata, ndata_overwrite):
    """Distribute data in space in place uniformly
    taking into account the occupied positions.
    
    Arguments:
    space -- 1-dimensional numpy array that represents space
    ndata -- total number of cells to write
    ndata_overwrite -- number of cells to overwrite
    """
    occupied_pos = space.nonzero()[0]
    occupied_cells = zeros(len(occupied_pos), dtype=bool)
    uniform(occupied_cells, ndata_overwrite)

    free_pos = (~space).nonzero()[0]
    free_cells = zeros(len(free_pos), dtype=bool)
    uniform(free_cells, ndata - min(ndata_overwrite, len(occupied_pos)))

    space.fill(False)
    space[occupied_pos] = occupied_cells
    space[free_pos] = free_cells


def normal(space, ndata):
    """Distribute data in space in place normally.
    
    Arguments:
    space -- 1-dimensional numpy array that represents space
    ndata -- total number of cells to write
    """
    if ndata >= len(space):
        space.fill(True)
        return

    mu, sigma = random.randint(space.size), space.size // 7
    positions = zeros(0, dtype=int)
    indices = zeros(0, dtype=int)
    while len(indices) < ndata:
        positions = hstack((positions, random.normal(mu, sigma, ndata).round().astype(int)))
        _, indices = unique(positions, return_index=True)

    indices.sort()
    space[positions[indices][:ndata] % space.size] = True


if __name__ == '__main__':
    from matplotlib import pyplot
    space = zeros(100, dtype=bool)
    normal(space, 40)    
    l = pyplot.plot(space,  'ro')
    pyplot.setp(l, markersize=5)
    pyplot.setp(l, markerfacecolor='C0')
    pyplot.show()