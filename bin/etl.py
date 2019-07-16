# -*- encoding: utf-8 -*-

"""
Script para extrair os registros do MongoDB e importá-los no HDFS.
"""

from watching.etl import ETL


def main():
    with ETL() as etl:
        etl.start()


if __name__ == '__main__':
    main()