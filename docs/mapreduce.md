# MapReduce

Copie o diretório "$WATCHING_HOME/watching/mapreduce" para "/tmp/cloudera/" para que ele seja acessível de dentro do container.

```shell
$ sudo cp -R $WATCHING_HOME/watching/mapreduce /tmp/cloudera/
```

Instale o Python 3 se ele não estiver instalado dentro do container.

```shell
$ docker container exec -it cloudera yum install -y python34
```

Execute o job de MapReduce.

```shell
$ docker container exec -it cloudera \
  sudo -u cloudera hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -files "/tmp/host/mapreduce" \
  -mapper "python3 /tmp/host/mapreduce/mapper_movies.py" \
  -reducer "python3 /tmp/host/mapreduce/reducer_movies.py" \
  -input "/user/cloudera/watching/posts/" \
  -output "/user/cloudera/watching/movies_posts_mentions_out/" 
```

Após a execução, o resultado estará no diretório "hdfs:///user/cloudera/watching/movies_posts_mentions_out".

Crie a tabela para manipular o arquivo gerado.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `watching`.`movies_posts_mentions`(
    `movie_id` STRING,
    `published_at` TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION "/user/cloudera/watching/movies_posts_mentions_out/";
```

Agora é possível gerar o arquivo com o conteúdo final.

> Para realizar consultas execute o Hive com o "hive-hcatalog-core.jar" carregado.

```sql
ADD JAR /usr/lib/impala/lib/hive-hcatalog-core.jar;

INSERT OVERWRITE DIRECTORY '/user/cloudera/watching/bi'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
COLLECTION ITEMS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
SELECT
    `mpm`.`published_at`,
    `m`.`id`,
    `m`.`original_title`,
    `m`.`ptbr_title`,
    `m`.`release_date`,
    `m`.`genres`,
    `m`.`cast`,
    `m`.`rating`,
    `m`.`votes`,
    `m`.`is_duplicated`
FROM `watching`.`movies_posts_mentions` `mpm`
    INNER JOIN `watching`.`movies` `m`
        ON (`mpm`.`movie_id`=`m`.`id`)
ORDER BY `mpm`.`published_at`;
```

Foi gerado um arquivo no formato CSV em "hdfs:///user/cloudera/watching/bi".

Cada linha deste arquivo representa o momento em que um determinado filme foi citado no Twitter. Há dados também sobre gênero, elenco, ano, nota e votos dos filmes.

Em especial a coluna "is_duplicated" indica que o título mencionado pode pertencer a dois filmes, sejam eles *remakes*/*reboots* ou dois filmes totalmente diferentes. Nestes casos é utilizado os dados do filmes mais recente.