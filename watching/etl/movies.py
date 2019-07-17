# -*- encoding: utf-8 -*-

import csv
import os
import re
import string
import json
import pymongo

from datetime import datetime

from bson.json_util import dumps

from watching.config import ETL_DIR

from watching.config import PROJECT_DIR
from watching.db import get_db
from watching.utils import dt_to_naive
from watching.utils import print_


class MoviesETL(object):

    def __init__(self):
        self.pat_double_spaces = re.compile(r'\s\s+', re.S)
        self.dataset_dir = os.path.join(PROJECT_DIR, 'datasets')
        self.datasets = {
            'movielens_credits': {'filename': os.path.join(self.dataset_dir, 'movielens-credits.csv'), 'data': None},
            'movielens_metadata': {'filename': os.path.join(self.dataset_dir, 'movielens-metadata.csv'), 'data': None},
            'ancine': {'filename': os.path.join(self.dataset_dir, 'ancine-movies.csv'), 'data': None},
        }

    def normalize_title(self, title):
        """ Trata um título de um filme.
        - Converte para minúsculo.
        - Remove pontuações.
        - Remove espaços duplos.
        """
        if not title:
            return None
        title = title.lower()
        title = title.translate(str.maketrans('', '', string.punctuation))
        title = self.pat_double_spaces.sub(' ', title).strip()
        if not title:
            title = None
        return title

    def title_versions(self, title):
        # spider-man -> spiderman
        # spider man -> spiderman
        pass

    def load_datasets(self):
        record_template = {
            'id': None,
            'en_title': None,
            'ptbr_title': None,
            'release_date': None,
            'cast': [],
            'score_avg': None,
        }
        print_('Processando dataset Ancine...')
        dataset = self.datasets['ancine']
        dataset['data'] = {}
        with open(dataset['filename'], 'r') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            reader.__next__()  # Ignora a primeira linha pois é o cabeçalho.
            for line in reader:
                id_, en_title, ptbr_title, release_date = line[0], line[1], line[2], line[5]
                release_date = datetime.strptime(release_date, '%Y-%m-%d')
                rec = record_template.copy()
                rec['en_title'] = self.normalize_title(en_title)
                rec['ptbr_title'] = self.normalize_title(ptbr_title)
                rec['release_date'] = release_date
                dataset['data'][rec['en_title']] = rec

        print_('Processando dataset MovieLens-Metadata...')
        dataset = self.datasets['movielens_metadata']
        dataset['data'] = {}
        with open(dataset['filename'], 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            reader.__next__()  # Ignora a primeira linha pois é o cabeçalho.
            for line in reader:
                rec = record_template.copy()
                genres, id_, en_title, release_date, score_avg, votes = line[3], line[5], line[8], line[14], line[22], line[23]
                rec['en_title'] = self.normalize_title(en_title)
                score_avg = float(score_avg)
                votes = int(votes)
                if votes < 10:
                    # Ignora filmes com poucos votos.
                    # print_('Filme ignorado - poucos votos: %s' % (rec['en_title']))
                    continue

                genres = eval(genres)
                genres = [g['name'] for g in genres]
                if not release_date:
                    # print_('Filme ignorado - sem data: %s' % (rec['en_title']))
                    continue

                rec['id'] = id_
                rec['genres'] = genres
                rec['score_avg'] = score_avg
                rec['release_date'] = release_date
                ancine = self.datasets['ancine']['data'].get(rec['en_title'])
                if ancine and ancine['ptbr_title']:
                    rec['ptbr_title'] = ancine['ptbr_title']
                dataset['data'][id_] = rec

        print_('Processando dataset MovieLens-Credits...')
        dataset = self.datasets['movielens_credits']
        dataset['data'] = {}
        with open(dataset['filename'], 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            reader.__next__()  # Ignora a primeira linha pois é o cabeçalho.
            for line in reader:
                rec = record_template.copy()
                cast, crew, id_ = line[0], line[1], line[2]
                cast = eval(cast)
                cast = [c['name'] for c in cast]
                dataset['data'][id_] = rec
                movie = self.datasets['movielens_metadata']['data'].get(id_)
                if movie:
                    movie['cast'] = cast

    def start(self):
        print_('Iniciando processamento de filmes...')
        self.load_datasets()
        filename = os.path.join(self.dataset_dir, 'movies-processed.csv')
        with open(filename, 'w') as f:
            for id_, movie in self.datasets['movielens_metadata']['data'].items():
                movie = json.dumps(movie)
                f.write('%s\n' % movie)
        print_('Finalizado')


if __name__ == '__main__':
    m = MoviesETL()
    m.start()