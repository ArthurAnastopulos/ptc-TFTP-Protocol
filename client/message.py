class Message:

    """Construtor da classe Message

    @param buffer: buffer contendo os dados da messagem
    """
    def __init__(self, buffer:str):
        self.__opcode = buffer[:2]
        self.__buffer = buffer

    """Faz a transmissão dos Dados das Mensagens

    """
    def serializeMsg(self):
        self._serial = bytearray()
        self.__serial += self.__buffer
        return self.__serial