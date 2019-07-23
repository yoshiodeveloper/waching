# Instalação e execução do Cloudera Quickstart 5.13

> Veja o documento de [docker.md](docker.md) para instruções de instalação.

Baixe a VM de quickstart na versão 5.13 da Cloudera. Escolha a opção *Docker Image*.

- https://www.cloudera.com/downloads/quickstart_vms/5-13.html

Descompacte o a imagem.

```shell
$ tar -zxvf cloudera-quickstart-vm-5.13.0-0-beta-docker.tar.gz
```

Importe a imagem.

```shell
$ docker run --hostname=quickstart.cloudera -v /tmp/cloudera:/tmp/host --privileged=true -t -i -d -p 8888:8888 -p 7180:80 --name cloudera cloudera/quickstart:5.13 /usr/bin/docker-quickstart
```

Repare que o diretório local "/tmp/cloudera" foi montado em "/tmp/host" dentro do container. Com isso é possível utilizar o "/tmp/cloudera" para enviar arquivos para o container manipular (ex: enviar os datasets do host para o container).

Verifique se os serviços estão subindo corretamente através dos logs.

```shell
$ docker container logs -f cloudera
```

Após alguns instantes o Hue estará acessível em http://localhost:8888. Utilize a login "cloudera" e senha "cloudera".
