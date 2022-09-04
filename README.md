<h1 align='center'>Projeto 1 - Protocolo <a href="https://datatracker.ietf.org/doc/html/rfc1350">TFTP</a> Cliente</h1>
<p align="center">Projeto de desenvolvimento de um cliente para o protocolo TFTP</p>

Tabela de conteúdos
=================
<!--ts-->
   * [Objetivos](#Objetivos)
   * [Pré-requisitos](#Pré-requisitos)
   * [Instruções para Uso](#Instruções-para-Uso)
   * [Máquina de Estado Finita do Protocolo TFTP](#Máquina-de-Estado-Finita-do-Protocolo-TFTP)
   * [Autores](#Autores)
<!--te-->

## Objetivos

1. **Desenvolver uma biblioteca**: o cliente do protocolo TFTP deve ser feito na forma de uma biblioteca, de forma que possa ser reutilizado em aplicações que precisem desse protocolo.
2. **Escrever um aplicativo demonstrativo**: usando sua biblioteca, deve-se criar um aplicativo capaz de enviar e receber arquivos usando o protocolo TFTP.

## Pré-requisitos

1. Instalar o progroma cliente e o servidor TFTP:
```bash
sudo apt install tftp atftpd
```

2. Instalar as dependências necessárias para a execução do projeto:
```bash
sudo apt update

sudo apt install python3
```
## Instruções para Uso

## Máquina de Estado Finita do Protocolo TFTP

<img align='center' src="images/state_machine_TFTP.png" width="850px;" alt=""></img>

## Autores

<a href="https://github.com/ArthurAnastopulos">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/51097061?v=4" width="100px;" alt=""/><br />
    <sub><b>Arthur Anastopulos dos Santos</b></sub></a><br />

<a href="https://github.com/alanamandim">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/58298192?v=4" width="100px;" alt=""/><br />
    <sub><b>Alana Mandim</b></sub></a><br />

<a href="https://github.com/jeffersonbcr">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/58866006?v=4" width="100px;" alt=""/><br />
    <sub><b>Jefferson Botitano</b></sub></a>

