from numpy import arange, hstack, count_nonzero, unique, zeros
from numpy.random import normal, randint


def sequential(space, startno, ndata):
    space.fill(False)
    remainder = max(0, ndata - (len(space) - startno))
    positions = hstack((arange(remainder), arange(startno, startno + ndata - remainder)))
    space[positions] = True


def uniform(space, ndata):
    space.fill(False)
    if ndata >= len(space):
        space.fill(True)
        return

    positions = zeros(0, dtype=int)
    indices = zeros(0, dtype=int)
    while len(indices) < ndata:
        positions = randint(0, len(space), 3 * ndata)
        _, indices = unique(positions, return_index=True)

    indices.sort()
    space[positions[indices][:ndata]] = True


def uniform_ow(space, ndata, ndata_overwrite):
    occupied_pos = space.nonzero()[0]
    occupied_cells = zeros(len(occupied_pos), dtype=bool)
    uniform(occupied_cells, ndata_overwrite)

    free_pos = (~space).nonzero()[0]
    free_cells = zeros(len(free_pos), dtype=bool)
    uniform(free_cells, ndata - min(ndata_overwrite, len(occupied_pos)))

    space.fill(False)
    space[occupied_pos] = occupied_cells
    space[free_pos] = free_cells



# def distribute_normal(space, ndata, mean=None, standart_deviation=None):
#     if ndata >= len(space):
#         space.fill(True)
#         return

#     if mean is not None and standart_deviation is not None:
#         if mean > space or mean < 0:
#             print('out of range of space')
#             return

#     if mean is None:
#         mean = len(space) // 2
#     if standart_deviation is None or standart_deviation > len(space) // 7:
#         standart_deviation = len(space) // 7

#     positions = []
#     while len(positions) < ndata:
#         positions = normal(mean, standart_deviation, 3 * ndata)
#         positions, indices = unique(positions.round().astype(int), return_index=True)

#     space[positions[indices.argsort()][:ndata] % len(space)] = True


# def distribute_normal_ow(space, ndata, ndata_overwrite, mean=None, standart_deviation=None):
#     occupied_pos = where(space)
#     occupied_cells = zeros(len(occupied_pos), dtype=bool)
#     occupied_mean = None if mean is None else mean * len(occupied_pos) // len(space)
#     occupied_deviation = None if mean is None else standart_deviation * len(occupied_pos) // len(space)
#     distribute_normal(occupied_cells, ndata_overwrite * ndata, occupied_mean, occupied_deviation)

#     free_pos = where(~space)
#     free_cells = zeros(len(free_pos), dtype=bool)
#     free_mean = None if mean is None else mean * len(free_pos) // len(space)
#     free_deviation = None if mean is None else standart_deviation * len(free_pos) // len(space)
#     distribute_normal(occupied_cells, (1 - ndata_overwrite) * ndata, free_mean, free_deviation)

#     space.fill(False)
#     space[occupied_pos] = occupied_cells
#     space[free_pos] = free_cells