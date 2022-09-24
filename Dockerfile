# Especificando tipo de image docker
FROM ubuntu:latest

# Atualizando image
RUN apt-get update

# Criando servidor TFTP
RUN sudo apt install tftp atftpd

# Adicionando diretório
WORKDIR /src

# Copiando data clientTFTP para diretório
COPY /dummy-files/ /src/