# -*- encoding: utf-8 -*-

"""
Script para extrair e tratar os datasets de filmes.
"""

from watching.etl.movies import MoviesETL


def main():
    with MoviesETL() as etl:
        etl.start()


if __name__ == '__main__':
    main()
