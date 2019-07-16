# -*- encoding: utf-8 -*-

import os
import pymongo

from datetime import datetime

from bson.json_util import dumps

from watching.config import ETL_DIR

from watching.db import get_db
from watching.utils import dt_to_naive
from watching.utils import print_


class ETL(object):
    """ Extrai os posts do MongoDB e gera arquivos para serem importado no HDFS.
    O formatos dos arquivos gerados é de um objeto json (registro) por linha.
    É gerado um diretório com a data e hora atual no local especificado em `ETL_DIR`. Os arquivos serão adicionados
    neste diretório separados por dia.
    """

    def __init__(self, start_dt=None, end_dt=None):
        """
        :param start_dt: Data inicial da extração em UTC-0.
        :param end_dt: Data final da extração em UTC-0.
        """
        self.now = dt_to_naive(datetime.utcnow())
        self.start_dt = dt_to_naive(start_dt)
        self.end_dt = dt_to_naive(end_dt) or self.now
        self.main_dump_dir = os.path.join(ETL_DIR, self.now.strftime('main-dump-%Y%m%d%H%M%S'))
        self.file_handlers = {}

    def __enter__(self):
        print_('Iniciando...')
        self.file_handlers = {}
        try:
            # Cria o diretório temporário se não existir.
            print_('Criando diretório principal em %s...' % self.main_dump_dir)
            os.makedirs(self.main_dump_dir)
        except FileExistsError:
            print_('O diretório principal já existe.')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for file_name, file_handler in self.file_handlers.items():
            print_('Fechando arquivo %s...' % file_name)
            file_handler.close()
        print_('Finalizado. Os arquivos extraídos se encontram em %s' % self.main_dump_dir)

    def get_file_handler(self, file_name):
        """ Retorna um file handler para inserir os registros JSON. """
        try:
            file_handler = self.file_handlers[file_name]
        except KeyError:
            full_filename = os.path.join(self.main_dump_dir, file_name)
            print_('Criando arquivo %s...' % full_filename)
            file_handler = open(full_filename, 'w')
            self.file_handlers[file_name] = file_handler
        return file_handler

    def start(self):
        db = get_db()
        find_params = {'tweet.retweeted_status': {'$exists': False}}
        if self.start_dt and self.end_dt:
            find_params['published_at'] = {'$gte': self.start_dt, '$lte': self.end_dt}
        elif self.start_dt:
            find_params['published_at'] = {'$gte': self.start_dt}
        elif self.end_dt:
            find_params['published_at'] = {'$lte': self.end_dt}
        print_('Consultando posts...')
        cursor = db.posts.find(find_params).sort([('published_at', pymongo.ASCENDING)])
        total = cursor.count()
        i = 0
        print_('Extraindo %d posts...' % total)
        for doc in cursor:
            file_name = 'dump-%s.json' % (doc['published_at'].strftime('%Y-%m-%d'))
            file_handler = self.get_file_handler(file_name)
            line = '%s\n' % dumps(doc)
            file_handler.write(line)
            if i % 1000 == 0:
                print_('%s de %s' % (i, total))
            i += 1
