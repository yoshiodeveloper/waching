# Instalação do Docker no Ubuntu 18.04/19.04

Instalando as dependências.

```shell
$ sudo apt-get update -y
$ sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

O comando abaixo deve listar o valor "0EBFCD88". Se o valor não for listado significa que as chaves não foram importadas corretamente.

```shell
$ apt-key adv --list-public-keys --with-colons | grep '^pub' | cut -d':' -f 5 | egrep -o '.{8}$'
```

Adicione o repositório do Docker. Repare que estamos instalando a versão "nightly", mas é possível utilizar a "stable" se preferir.

```shell
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) nightly"
$ sudo apt-get update -y
```

Agora é possível instalar o Docker e habilitar a execução no boot.

```shell
$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io
$ sudo systemctl enable docker
```

Adicione seu usuário no grupo "docker". Troque "$USER" pelo seu usuário se preferir.

```shell
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```

É necessário reiniciar o ambiente gráfico (Desktop) ou fazer um reboot na VM para funcionar a aplicação do grupo.

```shell
reboot
```