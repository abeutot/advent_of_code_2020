def str_to_seat(str_):
    assert len(str_) == 10
    assert set(str_[:7]) <= set('FB')
    assert set(str_[7:]) <= set('RL')

    min_row, max_row = 0, 127
    min_col, max_col = 0, 7

    for r in str_[:7]:
        # print('read:', r, 'min_row:', min_row, 'max_row:', max_row)
        if r == 'F':
            max_row -= (max_row - min_row) // 2 + 1
            continue
        if r == 'B':
            min_row += (max_row - min_row) // 2 + 1
            continue

    for c in str_[7:]:
        # print('read:', c, 'min_col:', min_col, 'max_col:', max_col)
        if c == 'R':
            min_col += (max_col - min_col) // 2 + 1
            continue
        if c == 'L':
            max_col -= (max_col - min_col) // 2 + 1
            continue

    assert max_row == min_row
    assert max_col == min_col

    # row, col, id
    return max_row, max_col, max_row * 8 + max_col


def test_samples():
    assert str_to_seat('FBFBBFFRLR') == (44, 5, 357)
    assert str_to_seat('BFFFBBFRRR') == (70, 7, 567)
    assert str_to_seat('FFFBBBFRRR') == (14, 7, 119)
    assert str_to_seat('BBFFBBFRLL') == (102, 4, 820)


if __name__ == '__main__':
    import sys
    from operator import itemgetter
    seats = list(map(str_to_seat, open(sys.argv[1]).read().rstrip('\n').split('\n')))
    print('max:', max(map(itemgetter(2), seats)))

    existing_seats_by_pos = {s[:2] for s in seats}
    existing_seats_by_id = {s[2] for s in seats}

    possible_rows = range(1, 127)
    possible_cols = range(1, 7)

    for r in possible_rows:
        for c in possible_cols:
            id_ = r * 8 + c
            if (r, c) not in existing_seats_by_pos and id_ + 1 in existing_seats_by_id and id_ - 1 in existing_seats_by_id:
                print((r, c, id_))
