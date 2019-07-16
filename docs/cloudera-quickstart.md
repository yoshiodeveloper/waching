Baixe a VM de quickstart na versão 5.13 da Cloudera. Escolha a opção **Docker Image**.

- https://www.cloudera.com/downloads/quickstart_vms/5-13.html

Descompacte o a imagem. 

- *Nota: A um problema no arquivo da Cloudera no qual ele foi transformado em ".tar" duas vezes. O procedimento reverso também deve ser feito duas vezes.*

```shell
$ gunzip cloudera-quickstart-vm-5.13.0-0-beta-docker.tar.gz
$ tar -xvf cloudera-quickstart-vm-5.13.0-0-beta-docker.tar   # este é um tar de um tar
```

Importe a imagem.

```shell
$ docker import cloudera-quickstart-vm-5.13.0-0-beta-docker/cloudera-quickstart-vm-5.13.0-0-beta-docker.tar cloudera/quickstart:5.13
```

Gere um container a partir da imagem.

```shell
$ docker run --hostname=quickstart.cloudera --privileged=true -t -i -d -p 8888:8888 -p 7180:80 --name cloudera cloudera/quickstart:5.13 /usr/bin/docker-quickstart
```

Verifique se os serviços estão subindo corretamente através dos logs.

```shell
$ docker container logs -f  cloudera
```

Acesse http://localhost:7180 e veja se a tela de "welcome" irá aparecer.

Após alguns instantes o Hue estará acessível em http://localhost:8888.