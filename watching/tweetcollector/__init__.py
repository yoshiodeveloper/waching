# -*- encoding: utf-8 -*-

import json
import pytz
import pymongo
import tweepy

from copy import deepcopy
from datetime import datetime
from time import sleep

from watching.config import (MONGO_DB, MONGO_URI, TWITTER_ACCESS_TOKEN,
                             TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                             TWITTER_TOKEN_SECRET, TWITTER_SEARCH_TERM)


class TweetCollector(object):
    """ Classe do coletor de tweets. """

    def __init__(self, run_forever=False, interval=30):
        """ Construtor da classe.

        :param run_forever: Indica para executar as buscas indefinidamente em intervalos.
        :param interval: Intervalo em segundos entre as buscas.
        """
        self.run_forever = run_forever
        self.interval = interval

    def print_(self, msg):
        """ Exibe um mensagem no terminal com a data atual. """
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('[%s] %s' % (dt, msg))

    def get_db(self):
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        return db

    def get_api(self):
        """ Retorna uma instância da API do Twitter. """
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)
        return tweepy.API(auth)

    def start(self):
        """ Inicia a coleta dos tweets. """
        while True:
            self.search_and_store()
            if self.run_forever:
                sleep(self.interval)
            else:
                break

    def search_and_store(self):
        """ Busca os tweets e armazena no DB. """
        db = self.get_db()
        api = self.get_api()
        tz = pytz.UTC
        q = TWITTER_SEARCH_TERM  # Termo de busca
        # TODO: Usar o since_id para especificar o último tweet coletado e evitar retonar muito tweets.

        inserted = 0

        # Pagina pelos resultados até encontrar algum tweet que já foi inserido.
        for tweepy_tweet in tweepy.Cursor(api.search, q=q, tweet_mode='extended', result_type='recent', count=100).items():
            tweet = deepcopy(tweepy_tweet._json)
            id_ = tweet['id']
            user = tweet.get('user') or {}
            screen_name = user.get('screen_name')
            published_at = tweet['created_at']
            published_at = datetime.strptime(published_at, '%a %b %d %H:%M:%S +0000 %Y')
            published_at = tz.localize(published_at)
            created_at = tz.localize(datetime.utcnow())
            text = tweet.get('full_text') or tweet.get('text') or ''
            resume = '%s #%s @%s: %s' % (published_at, id_, screen_name, text)
            post = {
                'source': 'Twitter',
                'context': q,
                'tweet': tweet,
                # 'facebook': ...
                # 'instagram': ...
                # 'youtube': ...
                'published_at': published_at,
                'created_at': created_at,
            }
            try:
                db.posts.insert(post)
            except pymongo.errors.DuplicateKeyError:
                break
            else:
                inserted += 1
                self.print_('[+] %s' % resume)

        self.print_('Tweets novos: %d' % inserted)