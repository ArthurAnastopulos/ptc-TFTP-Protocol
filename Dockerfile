# Especificando tipo de image docker
FROM ubuntu:latest

# Atualizando image
RUN apt-get update

# Criando servidor TFTP
RUN apt-get install xinetd tftpd tftp -y

COPY /tftp /etc/xinetd.d/tftp 

RUN mkdir /tftpboot

RUN chmod -R 777 /tftpboot

RUN chown -R nobody /tftpboot

RUN service xinetd restart

COPY files-tftp-server/ /tftpboot


