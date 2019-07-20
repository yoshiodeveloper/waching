# Hive

## Database

```sql
CREATE DATABASE IF NOT EXISTS watching;
```

## Tabela de filmes

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS watching.movies(
    id STRING,
    original_title STRING,
    ptbr_title STRING,
    release_date DATE
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
LOCATION "/user/watching/movies/"
```

## Tabela de posts (tweets)


```sql
CREATE EXTERNAL TABLE IF NOT EXISTS watching.movies_by_hour(
    published_at TIMESTAMP,
    movie_id STRING,
    `count` INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES("input.regex" = "([^|]+)\\|(\\d+)\\t(\\d+)")
STORED AS TEXTFILE
LOCATION "/user/watching/posts_out/";
```

Sempre execute o Hive com o "hive-hcatalog-core.jar".

```sql
ADD JAR /usr/lib/impala/lib/hive-hcatalog-core.jar;
```