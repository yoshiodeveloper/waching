# -*- encoding: utf-8 -*-

import os
import json

from watching.config import PROJECT_DIR
from watching.db import get_db
from watching.utils import print_


class PostsETL(object):

    def __init__(self):
        self.dataset_dir = os.path.join(PROJECT_DIR, 'datasets')

    def start(self):
        db = get_db()
        print_('Consultando posts...')
        posts_filename = os.path.join(self.dataset_dir, 'posts.json')
        posts = db.posts.find({}, {'published_at': 1, 'tweet.full_text': 1})
        total = posts.count()
        i = 0
        print_('Extraindo...')
        with open(posts_filename, 'w') as f:
            for doc in posts:
                if i % 1000 == 0:
                    print_('\textraído %s de %s...' % (i, total))
                published_at = doc.get('published_at').strftime('%Y-%m-%d %H:%M:%S.%f')
                full_text = doc.get('tweet', {}).get('full_text')
                rec = {'published_at': published_at, 'full_text': full_text}
                f.write('%s\n' % json.dumps(rec))
                i += 1
        print_('Finalizado')


if __name__ == '__main__':
    m = PostsETL()
    m.start()
