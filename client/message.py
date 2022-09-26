class Message:

    """Construtor da classe Message

    @param buffer: buffer contendo os dados da messagem
    """
    def __init__(self, buffer):
        #Verfica qual o tipo de mensagem foi recebido
        if type(buffer) != int:
            self.__opcode = buffer[1]
            self.__buffer = buffer
        else:
            self.__opcode = buffer

    """Obtem o Opcode da Mensagem

    @returns: Retorna o valor do Opcode
    """
    def getOpcode(self):
        return self.__opcode

    def getBuffer(self):
        return self.__buffer

    """Faz a transmissão dos Dados das Mensagens

    """
    def serializeMsg(self):
        serial = bytearray()
        serial += self.__buffer
        return serial