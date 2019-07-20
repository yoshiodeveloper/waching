#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import sys


def main(args):
    key = None
    last_key = None
    total = 0
    for line in sys.stdin:
        key, value = line.strip().split('\t', 1)
        value = int(value)

        if last_key is None:
            last_key = key

        if key == last_key:
            total += value
        else:
            print('%s\t%d' % (last_key, total))
            last_key = key
            total = 0
    if last_key is not None and (key == last_key):
        print('%s\t%d' % (last_key, total))


if __name__ == '__main__':
    main(sys.argv)
