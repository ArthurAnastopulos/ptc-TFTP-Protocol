from asyncio.log import logger
import sys
import logging as logger
from client import clientTftp

if len(sys.argv) == 0:
    logger.info('No argument was passed, exiting test program.')
    sys.exit()

# Capture os argumentos necessários para usar o programa de teste TFTP.
try:
    IP_ = sys.argv[1]
    logger.info('IP obtained by argument successfully') 
except Exception as Argument:
    logger.exception('Error. There is no IP passed by argument: \n', Argument)
    sys.exit()

try:
    PORT_ = sys.argv[2]
    logger.info('PORT obtained by argument successfully') 
except Exception as Argument:
    logger.exception('Error. There is no PORT passed by argument: \n', Argument)
    sys.exit()

try:
    TIMEOUT_ = sys.argv[3]
    logger.info('TIMEOUT obtained by argument successfully') 
except Exception as Argument:
    logger.exception('Error. There is no TIMEOUT passed by argument: \n', Argument)
    sys.exit()

try:
    FILENAME_ = sys.argv[4]
    logger.info('FILENAME obtained by argument successfully') 
except Exception as Argument:
    logger.exception('Error. There is no FILENAME passed by argument: \n', Argument)
    sys.exit()

try:
    REQUEST_ = sys.argv[5]
    logger.info('REQUEST obtained by argument successfully') 
except Exception as Argument:
    logger.exception('Error. There is no REQUEST passed by argument: \n', Argument)
    sys.exit()

MODE_ = "NetAscii"
if len(sys.argv) >= 6:
    try:
        MODE_ = sys.argv[6]
        logger.info('MODE obtained by argument successfully') 
    except Exception as Argument:
        logger.exception('Error. There is no REQUEST passed by argument: \n', Argument)
        sys.exit()
 
 # Inicia a classe do cliente TFTP com os argumentos obtidos. Se REQUEST_ tem seu opcode = 1 é um RRQ, ou se REQUEST_ tem seu opcode = 2 é um WRQ.
 # Qualquer outra coisa é um argumento REQUEST_ inválido, então o Cliente TFTP deve lançar uma mensagem de erro se outro opcode diferente de 1 ou 2 estiver na solicitação.
CLIENT = clientTftp

if REQUEST_ == 1:
    try:
        CLIENT.put()
    except Exception as Argument:
        logger.exception('Error. Error got while reading using TFTP: \n', Argument)
        sys.exit()  
elif REQUEST_ == 2:
    try:
        CLIENT.get()
    except Exception as Argument:
        logger.exception('Error. Error got while writing using TFTP: \n', Argument)
        sys.exit()
else:
    logger.info('This is an invalid opcode for the TFTP request, the expected response is an error on both types of requests.') 
    try:
        CLIENT.get()
        CLIENT.put()
    except Exception as Argument:
        logger.exception('Error. Error got while using wrong opcode for TFTP request: \n', Argument)
        sys.exit()