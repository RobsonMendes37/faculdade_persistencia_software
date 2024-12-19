import psycopg2
from psycopg2 import OperationalError

def get_connection():
    return psycopg2.connect(
        database="hospital-persistencia-lista8",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

def create_tables():
    try:
        connection = get_connection()  # Função para obter conexão com o banco de dados
        cursor = connection.cursor()
        print("Conectou e está iniciando")

        # Comandos para criação das tabelas
        commands = [
            """
            CREATE TABLE IF NOT EXISTS paciente (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                idade INT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sintoma (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                tratamento TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS paciente_sintoma (
                paciente_id INT NOT NULL REFERENCES paciente(id) ON DELETE CASCADE,
                sintoma_id INT NOT NULL REFERENCES sintoma(id) ON DELETE CASCADE,
                PRIMARY KEY (paciente_id, sintoma_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS medico (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                idade INT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS remedio (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                data_fabricacao DATE NOT NULL,
                data_validade DATE NOT NULL,
                prescricao TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS receita (
                id SERIAL PRIMARY KEY,
                medico_id INT NOT NULL REFERENCES medico(id) ON DELETE CASCADE,
                remedio_id INT NOT NULL REFERENCES remedio(id) ON DELETE CASCADE,
                paciente_id INT NOT NULL REFERENCES paciente(id) ON DELETE CASCADE
            )
            """
        ]


        for command in commands:
            cursor.execute(command)

        connection.commit()
        print("Tabelas criadas com sucesso.")

    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()



# Criação das tabelas no banco
create_tables()