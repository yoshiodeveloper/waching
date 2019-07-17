# watching

Trabalho sobre Hadoop feito em Python.
O sistema monitora tweets com o termo "assistindo" e armazena em uma base MongoDB.

Os tweets coletados são posteriormente processados pelo Hadoop para identificar os filmes que as pessoas estão assistindo.


## Instalação no Linux

> É necessário ter o Python 3, virtualenv e MongoDB instalados.

Crie um virtualenv.

```shell
$ virtualenv -p python3 venv
```

Ative o ambiente.

```shell
$ source venv/bin/activate
```

Instale as libs do Python no ambiente utilizando o arquivo "requirements.txt".

```shell
$ pip install -r requirements.txt
```

É necessário que o MongoDB esteja instalado e rodando em "127.0.0.1:27017".


## Execução do coletor de tweets

Configure a variável de ambiente.

```shell
export PYTHONPATH=$PYTHONPATH:/caminho/do/watching
```

> Repare que há um diretório "watching" dentro de "watching". O PYTHONPATH deve apontar para "/caminho/do/watching" e não para "/caminho/do/watching/watching".

> **Importante**: Esta forma de execução é apenas para o ambiente de desenvolvimento. Não deve ser executado desta forma em produção.

Para iniciar a coleta dos tweets:
```shell
python bin/collecttweets.py --run-forever
```

| Parâmetro | Descrição |
|--|--|
| --run-forever | Mantém o programa em execução realizando as buscas em intervalos. Padrão `False`. |
| --interval _INTERVAL_ | Intervalo em segundos das buscas. Usado em conjunto com o `--run-forever`. Padrão 30 segundos.|

Qualquer dúvida entre em contato: yoshiodeveloper@gmail.com
