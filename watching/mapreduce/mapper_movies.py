#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import re
import json
import sys

from moviestitles import MOVIES_TITLES

pat_double_spaces = re.compile(r'\s\s+', re.S|re.M)
pat_invalid_chars = re.compile(r'[|\\/@¨&*()–_–=–+§¬¹²³£¢\[\]\{\}<>!?¡¿,.;:§~¡¿ß´’"“”#$\'«»、。「」※…\n\t\r]+', re.S | re.M)


def normalize_title(title):
    if not title:
        return None
    title = title.lower()
    title = pat_invalid_chars.sub(' ', title).strip()
    # Exemplo "superman - o retorno" se transforma em "superman o retorno".
    # É diferente de "spider-man" onde deve continuar como "spider-man".
    title = title.replace(' - ', ' ')
    title = pat_double_spaces.sub(' ', title).strip()
    if not title:
        title = None
    return title


def main(args):
    for movie in MOVIES_TITLES:
        movie['words_count'] = len(movie['title'].split(' '))
        movie['title'] = ' assistindo %s ' % movie['title']
    for line in sys.stdin:
        try:
            line = json.loads(line)
        except:
            continue
        full_text = line['full_text']
        if full_text.startswith('RT @'):
            # Não precisa processar RTs.
            continue
        full_text = ' %s ' % normalize_title(full_text)
        for movie in MOVIES_TITLES:
            if movie['title'] in full_text:
                if (movie['words_count'] <= 2) and (movie['score'] < 10.0):
                    continue
                if (movie['words_count'] <= 3) and (movie['score'] < 9):
                    continue
                k = movie['movie_id']
                v = line['published_at']
                print('%s\t%s' % (k, v))
                break


if __name__ == '__main__':
    main(sys.argv)
