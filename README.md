# Watching

Trabalho do curso de Big Data sobre processamento paralelo utilizando Python, conceitos de crawling, MongoDB e Hadoop (HDFS, MapReduce e Hive).

O sistema monitora tweets com o termo "assistindo" que são posteriormente processados para identificar os filmes mencionados.

Foi utilizado datasets de filmes da Ancine e do IMDB. O dataset final gerado pelo sistema possui informações sobre a data e hora do tweet e título, ano, gênero, elenco, nota e votos do filme mencionado no tweet.

Este dataset pode ser importado em uma ferramenta de BI para análise das informações.

## Fluxo de uso

Sequência de documentações a serem seguidas para a execução do sistema:

- [Configuração no Linux](environment.md)
- [Instalação do MongoDB](mongodb.md)
- [Execução do crawler](crawler.md)
- [Instalação o Docker](docker.md)
- [Importar imagem Docker do Cloudera Quickstart](cloudera-quickstart.md)
- [Criação dos datasets e tabelas no Hive](datasets-and-hive.md)
- [Execução do MapReduce e geração do dataset final](mapreduce.md)


Qualquer dúvida entre em contato: yoshiodeveloper@gmail.com
