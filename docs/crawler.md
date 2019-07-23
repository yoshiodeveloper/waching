# Crawler

O crawler é responsável por coletar os tweets com o termo "assistindo". Ele utiliza a API REST do Twitter e por isso necessita de um app do Twitter para funcionar.

Crie o app no [Twitter Developers](https://developer.twitter.com/apps). Preencha as seguintes variáveis que estão em "$WATCHING_HOME/config.py".

- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_TOKEN_SECRET

Para iniciar a coleta dos tweets:

```shell
python $WATCHING_HOME/bin/collecttweets.py --run-forever
```

Este comando irá executar o crawler indefinidamente. Aperte CTRL+C para pará-lo.

| Parâmetro | Descrição |
|--|--|
| --run-forever | Mantém o programa em execução realizando as buscas em intervalos. Padrão `False`. |
| --interval _INTERVAL_ | Intervalo em segundos das buscas. Usado em conjunto com o `--run-forever`. Padrão 30 segundos.|

Outra opção é configurá-lo via "crontab". Use o script "$WATCHING_HOME/bin/collecttweets.sh".

```shell
$ contrab -e
```

Adicione a seguinte linha no crontab.

```shell
*/2       *      *       *       *       $WATCHING_HOME/bin/collecttweets.sh >> /tmp/collecttweets.log 2>&1
```

> O intervalo ideal é ciclos de 2 minutos no crontab.