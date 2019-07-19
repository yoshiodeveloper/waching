# Enviando datasets para o HDFS

Crie os diretórios dentro do HDFS onde ficação os datasets analisados.

```shell
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -mkdir -p /user/watching/movies
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -mkdir -p /user/watching/posts
```

Se o container não foi iniciado com um diretório montado (/tmp/cloudera) do host onde estão os datasets, pode-se importar os datasets no HDFS via Hue File Browser (http://localhost:8888/hue/home/) ou copiar para dentro do container e depois copiar para o HDFS.


## Via diretório montado

Crie o container com a opção "-v". Veja o documento "cloudera-quickstart.md". O container criado monta o diretório "/tmp/docker" ao diretório "/tmp/docker" do container.

```shell
$ sudo cp watching/datasets/movies-titles.json /tmp/cloudera/movies-titles.json
$ sudo cp watching/datasets/movies-processed.json /tmp/cloudera/movies-processed.json
$ sudo cp watching/datasets/posts.json /tmp/cloudera/posts.json
```

Insere no HDFS:

```shell
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -copyFromLocal /tmp/host/movies-processed.json /user/watching/movies/
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -copyFromLocal /tmp/host/posts.json /user/watching/posts/
```

## Via Hue File Browser

Acesse http://localhost:8888/hue/home/ e faça a inclusão dos arquivos no HDFS por lá.

## Via copiar local para dentro do container

> Esta forma não é recomendada, pois se os datasets forem grandes o container irá "inchar" em tamanho.

Copie os arquivos locais para dentro do container:

```shell
$ docker cp watching/datasets/movies-titles.json cloudera:/tmp/movies-titles.json
$ docker cp watching/datasets/movies-processed.json cloudera:/tmp/movies-processed.json
```

Insere do HDFS:

```shell
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -copyFromLocal /tmp/movies-titles.json /user/watching/movies-titles/
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -copyFromLocal /tmp/movies-processed.json /user/watching/movies/
```


## Extrair tweets do MongoDB


mongoexport --db watching --collection posts --type json --out posts.json 