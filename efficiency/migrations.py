def cow(source, snapshot):
    return sum(source * snapshot)


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
        current = removed.copy()
        current.fill(False)
        for i in range(snapshots.maxlen - 1):
            next_snap = snapshots.popleft()
            next_migr = (next_snap != migr) * migr
            snapshots.append((migr != next_migr) + current)
            current = next_snap
            migr = next_migr
            if not sum(migr):
                snapshots.append(current)
                #snapshots.maxlen - i + 1
                snapshots.rotate(-snapshots.maxlen + i + 2)
                break
        else:
            snapshots.append(current + migr)
        
        rest = snapshots.popleft()
        snapshots.appendleft(rest)
        return sum(removed) - sum(rest)
    else:
        return 0


if __name__ == '__main__':
    pass