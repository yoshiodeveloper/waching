# -*- encoding: utf-8 -*-

import sys


def main(args):
    for line in sys.stdin:
        print(line.strip())


if __name__ == '__main__':
    main(sys.argv)
