# -*- encoding: utf-8 -*-

import csv
import json
import re
import os

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
        self.mapreduce_dir = os.path.join(PROJECT_DIR, 'mapreduce')
        self.datasets = {
            'imdb_movies': {'filename': os.path.join(self.dataset_dir, 'imdb-movies.tsv'), 'data': None},
            'ancine': {'filename': os.path.join(self.dataset_dir, 'ancine-movies.csv'), 'data': None},
        }
        self.stopwords = ('a', 'as', 'às', 'ás', 'o', 'os', 'of', 'da', 'das', 'de', 'des', 'do', 'dos', 'du', 'la', 'lá', 'las', 'lo', 'los', 'que', 'the', 'that', 'this', 'um', 'uma', 'uns', 'umas', 'crônicas', 'cronicas', 'chronicles', 'saga')
        self.stopwords = {' %s ' % c for c in self.stopwords}
        self.record_template = {
            'id': None,
            'original_title': None,
            'ptbr_title': None,
            'scored_titles': [],
            'release_date': None,
            'genres': [],
            'cast': [],
            'rating': None,
            'votes': None,
            'is_duplicated': False,
        }

    def __enter__(self):
        print_('Iniciando...')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print_('Finalizado.')

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

    def get_ancine_dataset(self):
        """ Retorna o dataset da Ancine. Um dicionário é retornado onde a chave o título do filme (original) e o valor
        é uma lista de filmes ordenado pelo ano de forma descendente.
        Isto é necessário pois caso haja filmes com nomes iguais será dado preferência para o filme lançado mais
        recentemente.
        """
        filename = os.path.join(self.dataset_dir, 'ancine-movies.csv')
        dataset = {}
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            reader.__next__()  # Ignora a primeira linha pois é o cabeçalho.
            for line in reader:
                id_, original_title, ptbr_title, year_production, director, release_date = line[0], line[1], line[2], line[3], line[4], line[5]
                rec = self.record_template.copy()
                rec['original_title'] = self.normalize_title(original_title)
                rec['ptbr_title'] = self.normalize_title(ptbr_title)
                if rec['ptbr_title'] == 'a ser definido':
                    continue
                rec['release_date'] = datetime.strptime(release_date, '%Y-%m-%d')
                movie_list = dataset.setdefault(rec['original_title'], [])
                movie_list.append(rec)
        for movie_list in dataset.values():
            movie_list.sort(key=lambda x: x['release_date'], reverse=True)
            if len(movie_list) > 1:
                for movie in movie_list:
                    movie['is_duplicated'] = True
        return dataset

    def get_imdb_dataset(self):
        """ Retorna o dataset do IMDB. Um dicionário é retornado onde a chave o título do filme (original) e o valor
        é uma lista de filmes ordenado pelo ano de forma descendente.
        Isto é necessário pois caso haja filmes com nomes iguais será dado preferência para o filme lançado mais
        recentemente.
        """
        filename = os.path.join(self.dataset_dir, 'imdb-movies.tsv')
        dataset = {}
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            for line in reader:
                rec = self.record_template.copy()
                id_, title, start_year, end_year, genres, cast, rating, votes = line[0], line[1], line[2], line[3], \
                                                                                line[4], line[5], line[6], line[7]
                rec['original_title'] = self.normalize_title(title)
                try:
                    start_year = int(start_year)
                except:
                    start_year = None
                try:
                    end_year = int(end_year)
                except:
                    end_year = None
                try:
                    rating = float(rating)
                except:
                    rating = None
                votes = int(votes)
                if votes < 10:
                    # Ignora filmes com poucos votos.
                    continue
                genres = [g.strip() for g in genres.split(',') if g.strip()]
                cast = [c.strip() for c in cast.split(',') if c.strip()]
                rec['id'] = id_
                rec['genres'] = genres
                rec['cast'] = cast
                rec['rating'] = rating
                rec['votes'] = votes
                rec['release_date'] = datetime(end_year or start_year, 1, 1)
                if not all((rec['genres'], rec['cast'], rec['rating'], rec['votes'], rec['release_date'])):
                    continue
                movie_list = dataset.setdefault(rec['original_title'], [])
                movie_list.append(rec)
        for movie_list in dataset.values():
            movie_list.sort(key=lambda x: x['release_date'], reverse=True)
        return dataset

    def start(self):
        print_('Caregando dataset Ancine...')
        ancine_dataset = self.get_ancine_dataset()

        print_('Caregando dataset IMDB...')
        imdb_dataset = self.get_imdb_dataset()

        print_('Mesclando datasets...')
        movies = []
        for original_title, ancine_movies in ancine_dataset.items():
            imdb_movies = imdb_dataset.get(original_title)
            if not imdb_movies:
                continue
            for imdb_movie in imdb_movies:
                found = False
                for ancine_movie in ancine_movies:
                    diff = imdb_movie['release_date'] - ancine_movie['release_date']
                    if abs(diff.days) <= 365:
                        rec = {
                            'id': imdb_movie['id'],
                            'original_title': ancine_movie['original_title'],
                            'ptbr_title': ancine_movie['ptbr_title'],
                            'scored_titles': self.get_scored_titles([ancine_movie['ptbr_title'],
                                                                     ancine_movie['original_title']]),
                            'release_date': ancine_movie['release_date'],
                            'genres': imdb_movie['genres'],
                            'cast': imdb_movie['cast'],
                            'rating': imdb_movie['rating'],
                            'votes': imdb_movie['votes'],
                            'is_duplicated': ancine_movie['is_duplicated'],
                        }
                        movies.append(rec)
                        found = True
                if found:
                    break

        movies.sort(key=lambda x: x['release_date'], reverse=True)

        print_('Gravando movies.json...')
        movies_filename = os.path.join(self.dataset_dir, 'movies.json')
        with open(movies_filename, 'w') as f:
            for movie in movies:
                movie['release_date'] = movie['release_date'].strftime('%Y-%m-%d')
                movie = json.dumps(movie)
                f.write('%s\n' % movie)

        print_('Gerando títulos ponderados de filmes...')
        movie_titles = []
        for movie in movies:
            for score, title in movie['scored_titles']:
                movie_titles.append((len(title), score, title, movie['id']))
        movie_titles.sort(reverse=True)

        print_('Gravando moviestitles.py...')
        # Gera um arquivo com os nomes os títulos ordenados pelo tamanho do título e pontuação.
        moviestitles_filename = os.path.join(self.mapreduce_dir, 'moviestitles.py')
        with open(moviestitles_filename, 'w') as f:
            f.write('MOVIES_TITLES = (\n')
            for len_title, score, title, id_ in movie_titles:
                rec = {'score': score, 'title': title, 'title_length': len(title), 'movie_id': id_}
                f.write('    %s,\n' % repr(rec))
            f.write(')\n')

        print_('Importante 1: Foi gerado o arquivo "%s". Ele deve ser enviado ao HDFS em "hdfs:///user/cloudera/watching/movies".' % (movies_filename))
        print_('Importante 2: Foi gerado o arquivo "%s". Ele deve ser utilizado no script de mapper do MapReduce.' % (moviestitles_filename))
