# Especificando tipo de image docker
FROM ubuntu:16.04

# Atualizando image
RUN apt-get update

# Criando servidor TFTP
RUN sudo apt install tftp atftpd

# Adicionando diretório
WORKDIR /serverDataTFTP

# Copiando data clientTFTP para diretório
COPY /files/ /serverDataTFTP