# -*- encoding: utf-8 -*-

"""
Script para extrair e tratar os datasets de filmes.
"""

from watching.etl.movies import MoviesETL


def main():
    if input('Esta operação irá sobrescrever "movies.json" e "moviestitle.py" atuais. Deseja continuar? (s/n) ') != 's':
        print('operação cancelada')
        exit(1)
    with MoviesETL() as etl:
        etl.start()


if __name__ == '__main__':
    main()
