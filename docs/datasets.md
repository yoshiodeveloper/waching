# Extrair tweets do MongoDB

Para extrair os posts do Tweet use o script "extractposts.py".

 ```shell
$ python extractposts.py
```

Será gerado um arquivo "posts.json" no diretório atual.


# Extrair os dados de filmes

Estes dados já foram gerados em encontram-se no diretório "datasets".


# Enviando datasets para o HDFS

Crie os diretórios dentro do HDFS onde ficação os datasets analisados.

```shell
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -mkdir -p /user/watching/movies
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -mkdir -p /user/watching/posts
```

Crie o container com a opção "-v". Veja o documento "cloudera-quickstart.md". O container criado monta o diretório "/tmp/docker" ao diretório "/tmp/docker" do container.

```shell
$ sudo cp movies.json /tmp/cloudera/movies.json
$ sudo cp posts.json /tmp/cloudera/posts.json
```

> Se o container não foi iniciado com um diretório montado (/tmp/cloudera) do host onde estão os datasets, pode-se importar os datasets no HDFS via Hue File Browser (http://localhost:8888/hue/home/) ou copiar para dentro do container e depois copiar para o HDFS.

Insere no HDFS:

```shell
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -copyFromLocal /tmp/host/movies.json /user/watching/movies/
$ docker container exec -it cloudera sudo -u hdfs hdfs dfs -copyFromLocal /tmp/host/posts.json /user/watching/posts/
```
