import logging

# Configuração básica do logger
def configure_logger():
    logger = logging.getLogger("hero_api")
    logger.setLevel(logging.INFO)

    # Configurando o formato do log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Criando um manipulador de arquivo para gravar os logs em 'app.log'
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)

    # Adicionando o manipulador ao logger
    logger.addHandler(file_handler)

    return logger

# Instanciando o logger
logger = configure_logger()
