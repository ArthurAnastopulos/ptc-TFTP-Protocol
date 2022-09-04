from client.message import Message

class Error(Message):

    """Construtor da classe de Error(Herdada da classe Message)

    @param buffer: buffer contendo os dados da messagem
    @param errorCode: Codgio do Erro
    @param errMsg: Mensagem de Error
    """
    def __init__(self, buffer: str, errorCode:str, errMsg:str):
        super().__init__(buffer)
        self.__errorCode:str
        self.__errMsg:str

    """Faz a transmissão dos Dados das Mensagens

    """
    def serializeMsg(self):
        return super().serializeMsg()
