# MapReduce

Entre no container da Cloudera.

```shell
$ docker container exec -it cloudera bash
```

Instale o Python 3.

```shell
# yum install -y python34
```

Execute o job de MapReduce.

```shell
$ sudo -u hdfs hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -files "mapreduce" -mapper "python3 mapreduce/mapper_movies.py" -reducer "python3 mapreduce/reducer_movies.py" -input "/user/watching/posts/" -output "/user/watching/posts_out/"
```