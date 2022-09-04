from client.message import Message

from client.message import Message

class Data(Message):

    """Construtor da classe de Data(Herdada da classe Message) possui um número de bloco e um campo de dados

    @param buffer: buffer contendo os dados da messagem
    @param blck: String de Block do pacote
    @param data: Contém os dados da Messagem
    """
    def __init__(self, buffer: str, block:str, data:str):
        super().__init__(buffer)
        self.__block = block
        self.__data = data
        
    """Faz a transmissão dos Dados das Mensagens

    """
    def serializeMsg(self):
        return super().serializeMsg()