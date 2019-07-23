# -*- encoding: utf-8 -*-

"""
Script para extrair os registros do MongoDB.
"""

from watching.etl.posts import PostsETL


def main():
    if input('Esta operação irá sobrescrever "posts.json" atual. Deseja continuar? (s/n) ') != 's':
        print('operação cancelada')
        exit(1)
    with PostsETL() as etl:
        etl.start()


if __name__ == '__main__':
    main()
