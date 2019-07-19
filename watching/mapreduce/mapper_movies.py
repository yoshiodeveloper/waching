#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import json
import sys

from moviestitles import MOVIES_TITLES


def main(args):
    for movie in MOVIES_TITLES:
        movie['title'] = ' %s ' % movie['title']
    for line in sys.stdin:
        try:
            line = json.loads(line)
        except:
            continue
        for movie in MOVIES_TITLES:
            full_text = line['full_text']
            if full_text.startswith('RT @'):
                # Não precisa processar RT
                continue
            full_text = ' %s ' % full_text.lower()
            if movie['title'] in full_text:
                dt = line['published_at'][:13]  # retorna 'YYYY-MM-DD HH'
                dt = '%s:00:00' % (dt)
                key = '%s|%s' % (dt, movie['movie_id'])
                print('%s\t%s' % (key, 1))
                break


if __name__ == '__main__':
    main(sys.argv)
