# -*- encoding: utf-8 -*-

"""
Script para configurar o banco de dados no MongoDB.
"""

import pymongo

from watching.config import MONGO_DB, MONGO_URI


def main():
    msg = '### Atenção! ###\nTodos os dados do banco de dados "%s" (%s) serão permanentemente apagados!\nEscreva "drop" para confirmar esta ação: ' % (MONGO_DB, MONGO_URI)
    res = input(msg)
    if res != 'drop':
        print('Cancelado')
        return
    
    client = pymongo.MongoClient(MONGO_URI)
    
    print('Removendo banco de dados "%s" (se houver).' % MONGO_DB)
    client.drop_database(MONGO_DB)
    client.close()

    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    print('Criando índice único em "tweet.id" na collection "posts"')
    db.posts.create_index('tweet.id', unique=True )
    
    print('Criando índice (decrescente) em "published_at" na colletion "posts"')
    db.posts.create_index([('published_at', pymongo.DESCENDING)])

    print('Criando índice (decrescente) em "created_at" na colletion "posts"')
    db.posts.create_index([('created_at', pymongo.DESCENDING)])

    print('Finalizado')


if __name__ == '__main__':
    main()
