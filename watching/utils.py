# -*- encoding: utf-8 -*-

import pytz

from datetime import datetime


TZ_UTC = pytz.UTC


def print_(msg):
    """ Exibe uma mensagem no terminal com a data atual. """
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s] %s' % (dt, msg))


def dt_to_naive(dt):
    """ Adiciona o timezone UTC no datetime.
    * Não é feita conversão da data. Apenas é alterado o tzinfo.
    """
    if dt is not None and not dt.tzinfo:
        dt = TZ_UTC.localize(dt)
    return dt