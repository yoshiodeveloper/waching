# Instalação do MongoDB no Ubuntu 18.04/19.04

Instalando o repositório.

```shell
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
$ echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
$ sudo apt-get update
```

Instale o MongoDB.

```shell
$ sudo apt-get install -y mongodb-org
```

Inicie o serviço. O Mongo será estará rodando por padrão em "127.0.0.1:27017".

```shell
$ sudo service mongod start
```

Para parar o serviço.

```shell
$ sudo service mongod stop
```
