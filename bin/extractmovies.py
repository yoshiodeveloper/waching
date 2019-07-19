# -*- encoding: utf-8 -*-

from watching.etl.movies import MoviesETL


def main():
    with MoviesETL() as etl:
        etl.start()


if __name__ == '__main__':
    main()
