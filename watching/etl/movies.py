# -*- encoding: utf-8 -*-

import csv
import os
import re
import json

from datetime import datetime
from unidecode import unidecode

from watching.config import PROJECT_DIR
from watching.utils import print_


class MoviesETL(object):

    def __init__(self):
        self.pat_double_spaces = re.compile(r'\s\s+', re.S|re.M)
        # Somente o caracter '-' não é removido. Será utilizado para identificar nomes como "spider-man".
        self.pat_invalid_chars = re.compile(r'[|\\/@¨&*()–_–=–+§¬¹²³£¢\[\]\{\}<>!?¡¿,.;:§~¡¿ß´’"“”#$\'«»、。「」※…\n\t\r]+', re.S | re.M)
        self.dataset_dir = os.path.join(PROJECT_DIR, 'datasets')
        self.datasets = {
            'movielens_credits': {'filename': os.path.join(self.dataset_dir, 'movielens-credits.csv'), 'data': None},
            'movielens_metadata': {'filename': os.path.join(self.dataset_dir, 'movielens-metadata.csv'), 'data': None},
            'ancine': {'filename': os.path.join(self.dataset_dir, 'ancine-movies.csv'), 'data': None},
        }
        self.stopwords = ('a', 'as', 'às', 'ás', 'o', 'os', 'of', 'da', 'das', 'de', 'des', 'do', 'dos', 'du', 'la', 'lá', 'las', 'lo', 'los', 'que', 'the', 'that', 'this', 'um', 'uma', 'uns', 'umas', 'crônicas', 'cronicas', 'chronicles', 'saga')
        self.stopwords = {' %s ' % c for c in self.stopwords}

    def normalize_title(self, title):
        """ Trata um título de um filme.
        - Converte para minúsculo.
        - Remove pontuações.
        - Remove espaços duplos.
        """
        if not title:
            return None
        title = title.lower()
        title = self.pat_invalid_chars.sub(' ', title).strip()
        # Exemplo "superman - o retorno" se transforma em "superman o retorno".
        # É diferente de "spider-man" onde deve continuar como "spider-man".
        title = title.replace(' - ', ' ')
        title = self.pat_double_spaces.sub(' ', title).strip()
        if not title:
            title = None
        return title

    def remove_stopwords(self, title):
        for c in self.stopwords:
            title = ' %s ' % title
            if c in title:
                title = title.replace(c, ' ')
        title = self.pat_double_spaces.sub(' ', title).strip()
        return title

    def get_scored_titles(self, titles):
        """ Gera uma lista de títulos com a porcentagem. """
        for t in titles[:]:
            if '-' in t:
                # spider-man -> spiderman, spider man
                titles.append(t.replace('-', ''))
                titles.append(t.replace('-', ' '))
        scored_titles = []
        for title in titles:
            a = title
            b = unidecode(a)  # remove os acentos
            c = self.remove_stopwords(b)
            d = self.remove_stopwords(a)
            rate = 10 / 4
            included = set()
            for w, text in ((4, a), (3, b), (2, c), (1, d)):
                parts = text.split(' ')
                total = len(parts)
                for idx, part in enumerate(parts):
                    t = ' '.join(parts[0:idx+1])
                    if len(t) < 2:
                        continue
                    if t in included:
                        continue
                    included.add(t)
                    perc = ((idx + 1) / total) * w * rate
                    scored_titles.append((perc, t))
        return scored_titles

    def load_datasets(self):
        record_template = {
            'id': None,
            'original_title': None,
            'ptbr_title': None,
            'scored_titles': [],
            'release_date': None,
            'cast': [],
            'score_avg': None,
        }
        movies_dataset = {}

        print_('Processando dataset Ancine...')
        dataset = self.datasets['ancine']
        dataset['data'] = {}
        with open(dataset['filename'], 'r') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            reader.__next__()  # Ignora a primeira linha pois é o cabeçalho.
            for line in reader:
                id_, original_title, ptbr_title, release_date = line[0], line[1], line[2], line[5]
                release_date = datetime.strptime(release_date, '%Y-%m-%d')
                rec = record_template.copy()
                rec['original_title'] = self.normalize_title(original_title)
                rec['ptbr_title'] = self.normalize_title(ptbr_title)
                rec['release_date'] = release_date
                dataset['data'][rec['original_title']] = rec

        print_('Processando dataset MovieLens-Metadata...')
        dataset = self.datasets['movielens_metadata']
        dataset['data'] = {}
        with open(dataset['filename'], 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            reader.__next__()  # Ignora a primeira linha pois é o cabeçalho.
            for line in reader:
                rec = record_template.copy()
                genres, id_, original_title, release_date, score_avg, votes = line[3], line[5], line[8], line[14], line[22], line[23]
                rec['original_title'] = self.normalize_title(original_title)
                score_avg = float(score_avg)
                votes = int(votes)
                if votes < 10:
                    # Ignora filmes com poucos votos.
                    # print_('Filme ignorado - poucos votos: %s' % (rec['original_title']))
                    continue

                genres = eval(genres)
                genres = [g['name'] for g in genres]
                if not release_date:
                    # print_('Filme ignorado - sem data: %s' % (rec['original_title']))
                    continue

                rec['id'] = id_
                rec['genres'] = genres
                rec['score_avg'] = score_avg
                rec['release_date'] = release_date
                ancine = self.datasets['ancine']['data'].get(rec['original_title'])
                if (not ancine) or (not ancine['ptbr_title']):
                    # Serão analisados apenas títulos com nome em português.
                    continue
                rec['ptbr_title'] = ancine['ptbr_title']
                rec['scored_titles'] = self.get_scored_titles([rec['ptbr_title'], rec['original_title']])
                movies_dataset[id_] = rec

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
                movie = movies_dataset.get(id_)
                if movie:
                    movie['cast'] = cast
        return movies_dataset

    def start(self):
        print_('Iniciando processamento de filmes...')
        movies = self.load_datasets()

        filename = os.path.join(self.dataset_dir, 'movies-processed.json')
        with open(filename, 'w') as f:
            for id_, movie in movies.items():
                movie = json.dumps(movie)
                f.write('%s\n' % movie)

        # Gera um arquivo com os nomes os títulos ordenados pelo tamanho do título e pontuação.
        movie_titles = []
        for id_, movie in movies.items():
            for score, title in movie['scored_titles']:
                movie_titles.append((len(title), score, title, id_))
        movie_titles.sort(reverse=True)

        filename = os.path.join(self.dataset_dir, 'movies-titles.json')
        with open(filename, 'w') as f:
            for len_title, score, title, id_ in movie_titles:
                rec = {'score': score, 'title': title, 'movie_id': id_}
                f.write('%s\n' % json.dumps(rec))

        print_('Finalizado')


if __name__ == '__main__':
    m = MoviesETL()
    m.start()
    
