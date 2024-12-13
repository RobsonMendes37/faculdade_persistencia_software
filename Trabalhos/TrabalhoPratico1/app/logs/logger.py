# Função para registrar logs
from datetime import datetime
import os


def enviar_log(message):
    # Caminho do arquivo de log
    log_file_path = 'app/utils/logs.txt'

    # Formatação da data e hora
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{current_time} - {message}\n"

    # Verifica se o arquivo de log existe
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as file: #cria o arquivo
            file.write(log_message)
            print("Arquivo de log criado e mensagem registrada")
    else:
        with open(log_file_path, 'a') as file:
            file.write(log_message)
            print("Mensagem registrada no log")
