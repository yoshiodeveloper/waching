# Configuração do ambiente no Ubuntu 18.04/19.04

Edite o arquivo "/home/$USER/.bashrc" e adicione esta linha no final do arquivo.

```shell
WATCHING_HOME="/caminho/do/watching"
```

Recarregue as configurações.

```bash
source "/home/$USER/.bashrc"
```

> Repare que há um diretório "watching" dentro de "watching". A variável $WATCHING_HOME deve apontar para "/caminho/do/watching" e não para "/caminho/do/watching/watching".

Instale o python-pip e python3-venv.

```bash
$ sudo apt-get update
$ sudo apt-get install -y python3-pip
$ sudo apt-get install -y python3-venv
```

Crie um [venv](https://docs.python.org/3/library/venv.html).

```bash
$ python3 -m venv $WATCHING_HOME/venv
```

Ative o ambiente criado.

```bash
$ source $WATCHING_HOME/venv/bin/activate
```

Instale as libs do Python no ambiente utilizando o arquivo "requirements.txt".

```bash
$ pip install -r $WATCHING_HOME/requirements.txt
```

Para executar os script inclua o diretório do Watching dentro do PYTHONPATH.

```bash
$ export PYTHONPATH=$PYTHONPATH:$WATCHING_HOME
$ python meuscript.py
```