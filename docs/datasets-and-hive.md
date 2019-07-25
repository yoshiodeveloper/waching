# Criação dos datasets

Para a criação dos datasets será necessário um container da Cloudera Quickstart.

> Veja o documento de [cloudera-quickstart.md](cloudera-quickstart.md) para instruções de instalação.

> Alguns datasets não precisam ser gerados, pois já estão inclusos no código fonte.

Crie o banco de dados "watching" no Hive. Pode ser feito via Hue (http://localhost:8888).

```sql
CREATE DATABASE IF NOT EXISTS `watching`;
```

Algumas consultas que manipulam JSON no Hive podem exigir o carregamento do "hive-hcatalog-core.jar". Execute este comando no Hive antes das consultas.

```sql
ADD JAR /usr/lib/impala/lib/hive-hcatalog-core.jar;
```

## Dataset posts.json

Para extrair os posts do Tweet use o script "extractposts.py".

 ```shell
$ python $WATCHING_HOME/bin/extractposts.py
```

Será gerado um arquivo "posts.json" em "watching/datasets".

Envie o dataset para o HDFS.

```shell
$ sudo cp $WATCHING_HOME/watching/datasets/posts.json /tmp/cloudera/
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -mkdir -p /user/cloudera/watching/posts
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -copyFromLocal /tmp/host/posts.json /user/cloudera/watching/posts/
```

Crie a tabela no Hive para o dataset.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `watching`.`posts`(
    `published_at` TIMESTAMP,
    `full_text` STRING
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
LOCATION '/user/cloudera/watching/posts/';
```

## Dataset imdb-movies.tsv

> O dataset "imdb-movies.tsv" já foi gerado em encontra-se no diretório "watching/datasets". Não é necessário gerá-lo novamente.

Os seguintes datasets podem ser obtidos no site do IMDB (https://www.imdb.com/interfaces/).

- title.basics.tsv.gz
- title.principals.tsv.gz
- name.basics.tsv.gz
- title.ratings.tsv.gz

Descompacte os arquivos.

```shell
$ gunzip -k -c title.basics.tsv.gz > imdb-titles.tsv
$ gunzip -k -c title.principals.tsv.gz > imdb-principals.tsv
$ gunzip -k -c name.basics.tsv.gz > imdb-names.tsv
$ gunzip -k -c title.ratings.tsv.gz > imdb-ratings.tsv
```

Envie ao HDFS.

```shell
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -mkdir -p /user/cloudera/imdb/titles
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -mkdir -p /user/cloudera/imdb/principals
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -mkdir -p /user/cloudera/imdb/names
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -mkdir -p /user/cloudera/imdb/ratings

$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -copyFromLocal imdb-titles.tsv /user/cloudera/imdb/titles/
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -copyFromLocal imdb-principals.tsv /user/cloudera/imdb/principals/
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -copyFromLocal imdb-names.tsv /user/cloudera/imdb/names/
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -copyFromLocal imdb-ratings.tsv /user/cloudera/imdb/ratings/
```

Crie as tabelas no Hive para cada dataset. Essas tabelas serão unificadas (join) para gerar o arquivo.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `watching`.`imdb_titles`(
    `tconst` STRING,
    `titleType` STRING,
    `primaryTitle` STRING,
    `originalTitle` STRING,
    `isAdult` INT,
    `startYear` INT,
    `endYear` INT,
    `runtimeMinutes` INT,
    `genres` ARRAY<STRING>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION "/user/cloudera/imdb/titles"
tblproperties ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS `watching`.`imdb_ratings`(
    `tconst` STRING,
    `averageRating` FLOAT,
    `numVotes` INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION "/user/cloudera/imdb/ratings"
tblproperties ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS `watching`.`imdb_names`(
    `nconst` STRING,
    `primaryName` STRING,
    `birthYear` INT,
    `deathYear` INT,
    `primaryProfession` ARRAY<STRING>,
    `knownForTitles` ARRAY<STRING>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION "/user/cloudera/imdb/names"
tblproperties ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS `watching`.`imdb_principals`(
    `tconst` STRING,
    `ordering` INT,
    `nconst` STRING,
    `category` STRING,
    `job` STRING,
    `characters` ARRAY<STRING>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION "/user/cloudera/imdb/principals"
tblproperties ("skip.header.line.count"="1");
```

Para gerar o arquivo "imdb-movies.tsv" execute o seguinte comando no Hive. O conteúdo do arquivo será gerado em "hdfs:///user/cloudera/imdb/imdb_out".

```sql
INSERT OVERWRITE DIRECTORY "/user/cloudera/imdb/imdb_out"
ROW FORMAT DELIMITED
FIELDS TERMINATED BY "\t"
COLLECTION ITEMS TERMINATED BY ','
LINES TERMINATED BY "\n"
STORED AS TEXTFILE
SELECT
    `t`.`tconst`,
    `t`.`originaltitle`,
    `t`.`startyear`,
    `t`.`endyear`,
    `t`.`genres`,
    CONCAT_WS(',', COLLECT_LIST(`n`.`primaryname`)) AS `cast`,
    `r`.`averageRating`,
    `r`.`numVotes`
FROM `imdb_titles` `t`
INNER JOIN `imdb_ratings` `r`
    ON `r`.`tconst`=`t`.`tconst`
INNER JOIN `imdb_principals` `p`
    ON `t`.`tconst`=`p`.`tconst`
INNER JOIN `imdb_names` `n`
    ON `n`.`nconst`=`p`.`nconst`
WHERE `t`.`titletype`='movie'
GROUP BY `t`.`tconst`, `t`.`originaltitle`, `t`.`startyear`, `t`.`endyear`, `t`.`genres`, `r`.`averagerating`, `r`.`numvotes`;
```

- Renomei o arquivo para "imdb-movies.tsv".
- Abra o arquivo utilizando o Excel e ordene as linhas pela coluna "startdate" em ordem decrescente e salve.
- Ao ordenar será possível verificar linhas problemáticas. Corrija ou elimine essas linhas e salve o arquivo.
- Copie o arquivo para o diretório "$WATCHING_HOME/watching/datasets".


## Dataset movies.json

> O dataset "movies.json" já foi gerado em encontra-se no diretório "$WATCHING_HOME/datasets". Não é necessário gerá-lo novamente.

Descompacte os arquivos ".gz" do diretório "$WATCHING_HOME/watching/datasets" e execute o script "$WATCHING_HOME/bin/extractmovies.py".

```shell
$ cd $WATCHING_HOME/watching/datasets
$ gzip -k ancine-movies.gz  # gera ancine-movies.csv
$ gzip -k imdb-movies.gz  # gera imdb-movies.tsv
$ python $WATCHING_HOME/bin/extractmovies.py
```

O script "extractmovies.py" irá utilizar os datasets "ancine-movies.csv" e "imdb-movies.tsv" para gerar o dataset "movies.json". Este dataset será gerado em "$WATCHING_HOME/watching/datasets".

Envie o dataset para o HDFS.

```shell
$ sudo cp $WATCHING_HOME/watching/datasets/movies.json /tmp/cloudera/
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -mkdir -p /user/cloudera/watching/movies
$ docker container exec -it cloudera sudo -u cloudera hdfs dfs -copyFromLocal /tmp/host/movies.json /user/cloudera/watching/movies/
```

Crie as tabelas no Hive para o dataset.

```sql
ADD JAR /usr/lib/impala/lib/hive-hcatalog-core.jar;

CREATE EXTERNAL TABLE IF NOT EXISTS `watching`.`movies`(
    `id` STRING,
    `original_title` STRING,
    `ptbr_title` STRING,
    `release_date` DATE,
    `cast` ARRAY<STRING>,
    `genres` ARRAY<STRING>,
    `rating` FLOAT,
    `votes` INT,
    `is_duplicated` BOOLEAN
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
LOCATION '/user/cloudera/watching/movies/';
```
