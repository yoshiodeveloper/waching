# -*- encoding: utf-8 -*-

"""
Script para realizar a coleta dos tweets.
"""

import argparse

from watching.tweetcollector import TweetCollector


parser = argparse.ArgumentParser(description='Coletor de tweets.')
parser.add_argument('--run-forever', action='store_true', help='O programa não é finalizado neste modo e as buscas são'
                                                               ' realizadas automaticamente em intervalos. Use'
                                                               ' "--interval" se desejar especificar o intervalo entre'
                                                               ' as buscas.')
parser.add_argument('--interval', type=int, default=30, help='Intervalo em segundo entre as buscas.')
args = parser.parse_args()


def main():
    collector = TweetCollector(run_forever=args.run_forever, interval=args.interval)
    collector.start()


if __name__ == '__main__':
    main()
