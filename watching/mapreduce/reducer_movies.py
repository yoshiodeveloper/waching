#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import sys


def main(args):
    for line in sys.stdin:
        print(line.strip())
        # ou
        # movie_id, published_at = line.strip().split('\t', 1)
        # ...
        # print('%s\t%s' % (movie_id, published_at))


if __name__ == '__main__':
    main(sys.argv)
