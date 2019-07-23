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
                # Não precisa processar RTs.
                continue
            full_text = ' %s ' % full_text.lower()
            if movie['title'] in full_text:
                #key = '%s|%s' % (line['published_at'], movie['movie_id'])
                k = movie['movie_id']
                v = line['published_at']
                print('%s\t%s' % (k, v))
                break


if __name__ == '__main__':
    main(sys.argv)
