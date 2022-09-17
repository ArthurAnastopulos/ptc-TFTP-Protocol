class Message:

    """Construtor da classe Message

    @param buffer: buffer contendo os dados da messagem
    """
    def __init__(self, buffer):
        #Verfica qual o tipo de mensagem foi recebido
        if type(buffer) != int:
            self.__opcode = buffer[:2]
            self.__buffer = buffer
        else:
            self.__opcode = buffer


    """Faz a transmissão dos Dados das Mensagens

    """
    def serializeMsg(self):
        serial = bytearray()
        serial += self.__buffer
        return serial