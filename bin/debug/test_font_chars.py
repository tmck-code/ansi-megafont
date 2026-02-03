#!/usr/bin/env python3
# visually test a font by rendering all chars from `0x00` > `0x7F`
# usage:
# ./ops/test_font_chars.py 0 2080

from itertools import batched
import sys


def test_font_chars(start: int, end: int) -> None:
    print(f'{start:#06x} to {end:#06x} character set:')

    pad_start, pad_end = start-(start % 16), end+(16-(end % 16))
    print(' '+'─'*162)
    for i, row in enumerate(batched(range(pad_start, pad_end), 16)):
        print('\n ', end='')
        for el in row:
            char = chr(el)
            print(f'│ {char:^8s}', end='')
        print(' │\n\n ', end='')
        for el in [f'{" ":^8s}' if el < start or el > end else f'{el:>#04x}' for el in row]:
            print(f'│ {el:^8s}', end='')
        print(' │\n\n '+'─'*162)

if __name__ == '__main__':
    start, end = 0x00, 0x7F
    if len(sys.argv) == 3:
        try:
            start = int(sys.argv[1], 16)
            print(f'start is hex: {start:X}')
        except ValueError:
            start = int(sys.argv[1])
            print('start is dec:', start)

        try:
            end = int(sys.argv[2], 16)
            print(f'end is hex: {end:X}')
        except ValueError:
            end = int(sys.argv[2])

        if end < start:
            end = start + int(sys.argv[2])
            print(f'end is offset: {end:X}')
        else:
            print(f'end is dec:', end)

    test_font_chars(start, end)
