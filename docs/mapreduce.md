Instale o Python 3 dentro do container da Cloudera.

```shell
# yum install -y python34
```

Execute o job de MapReduce.

```shell
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -files "mapreduce" -mapper "python3 mapreduce/mapper_movies.py" -reducer "python3 mapreduce/reducer_movies.py" -input "/user/watching/posts/" -output "/user/watching/posts_out/"
```