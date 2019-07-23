# -*- encoding: utf-8 -*-

import os
import json

from datetime import datetime

from watching.config import PROJECT_DIR
from watching.db import get_db
from watching.utils import print_


class PostsETL(object):

    def __init__(self):
        self.dataset_dir = os.path.join(PROJECT_DIR, 'datasets')

    def __enter__(self):
        print_('Iniciando...')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print_('Finalizado.')

    def start(self):
        db = get_db()
        print_('Consultando posts no MongoDB...')
        filename = os.path.join(self.dataset_dir, 'posts.json')
        #start_at = datetime(2019, 7, 8, 0, 0, 0, 0)
        # end_at = datetime(2019, 7, 14, 23, 59, 59, 999999)
        #find_filter = {'published_at': {'$gte': start_at, '$lte': end_at}}
        find_filter = {}
        posts = db.posts.find(find_filter, {'published_at': 1, 'tweet.full_text': 1})
        total = posts.count()
        i = 0
        print_('Extraindo...')
        with open(filename, 'w') as f:
            for doc in posts:
                i += 1
                if i % 1000 == 0:
                    print_('\textraído %s de %s...' % (i, total))
                if i % 10 != 0:
                    continue
                published_at = doc.get('published_at').strftime('%Y-%m-%d %H:%M:%S.%f')
                full_text = doc.get('tweet', {}).get('full_text')
                rec = {'published_at': published_at, 'full_text': full_text}
                f.write('%s\n' % json.dumps(rec))

        print_('Importante: Foi gerado o arquivo "%s". Ele deve ser enviado ao HDFS em "hdfs:///user/cloudera/watching/posts".' % (filename))
