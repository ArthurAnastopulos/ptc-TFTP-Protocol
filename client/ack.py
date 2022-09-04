from client.message import Message

class Ack(Message):

    """Construtor da classe de Ack(Herdada da classe Message) usado para ser reconhecido pelos pacotes DATA e ERROR

    @param buffer: buffer contendo os dados da messagem
    @param blck: String de Block do pacote
    @param data: Contém os dados da Messagem
    """
    def __init__(self, buffer: str, block:str):
        super().__init__(buffer)
        self.__block = block

    """Faz a transmissão dos Dados das Mensagens

    """
    def serializeMsg(self):
        return super().serializeMsg()