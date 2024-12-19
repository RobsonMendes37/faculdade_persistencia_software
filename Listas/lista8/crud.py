from datetime import date
from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from bd_connection import get_connection

#-------------------CRUD para Paciente------------------

#Criar
def criar_paciente(nome:str, idade:int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO paciente (nome, idade) VALUES (%s, %s) RETURNING id", (nome, idade))
    paciente_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return paciente_id

#Listar
def listar_pacientes():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM paciente")
    pacientes = cursor.fetchall()
    connection.close()
    return pacientes

#Atualizar
def atualizar_paciente_no_bd(paciente_id: int, nome: str = None, idade: int = None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o paciente existe
        cursor.execute("SELECT * FROM paciente WHERE id = %s", (paciente_id,))
        paciente = cursor.fetchone()
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")

        # Atualizar os campos se houverem novos valores
        if nome:
            cursor.execute("UPDATE paciente SET nome = %s WHERE id = %s", (nome, paciente_id))
        if idade:
            cursor.execute("UPDATE paciente SET idade = %s WHERE id = %s", (idade, paciente_id))

        conn.commit()
    finally:
        cursor.close()
        conn.close()


#Deletar
def deletar_paciente_no_bd(paciente_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o paciente existe
        cursor.execute("SELECT * FROM paciente WHERE id = %s", (paciente_id,))
        paciente = cursor.fetchone()
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")

        # Deletar o paciente
        cursor.execute("DELETE FROM paciente WHERE id = %s", (paciente_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()



#-----------------------CRUD para Medico----------------------

# Criar
def criar_medico(nome: str, idade: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO medico (nome, idade) VALUES (%s, %s) RETURNING id", (nome, idade))
    medico_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return medico_id

# Listar
def listar_medicos():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM medico")
    medicos = cursor.fetchall()
    connection.close()
    return medicos

# Atualizar
def atualizar_medico_no_bd(medico_id: int, nome: str = None, idade: int = None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o medico existe
        cursor.execute("SELECT * FROM medico WHERE id = %s", (medico_id,))
        medico = cursor.fetchone()
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")

        # Atualizar os campos se houverem novos valores
        if nome:
            cursor.execute("UPDATE medico SET nome = %s WHERE id = %s", (nome, medico_id))
        if idade:
            cursor.execute("UPDATE medico SET idade = %s WHERE id = %s", (idade, medico_id))

        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Deletar
def deletar_medico_no_bd(medico_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o medico existe
        cursor.execute("SELECT * FROM medico WHERE id = %s", (medico_id,))
        medico = cursor.fetchone()
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")

        # Deletar o medico
        cursor.execute("DELETE FROM medico WHERE id = %s", (medico_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


#----------------------------CRUD Sintoma-----------------------

# Criar Sintoma
def criar_sintoma(nome: str, tratamento: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO sintoma (nome, tratamento) VALUES (%s, %s) RETURNING id", (nome, tratamento))
    sintoma_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return sintoma_id

# Listar Sintomas
def listar_sintomas():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM sintoma")
    sintomas = cursor.fetchall()
    connection.close()
    return sintomas

# Atualizar Sintoma no banco de dados
def atualizar_sintoma_no_bd(sintoma_id: int, nome: str = None, tratamento: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o sintoma existe
        cursor.execute("SELECT * FROM sintoma WHERE id = %s", (sintoma_id,))
        sintoma = cursor.fetchone()
        if not sintoma:
            raise HTTPException(status_code=404, detail="Sintoma não encontrado")

        # Atualizar os campos se houverem novos valores
        if nome:
            cursor.execute("UPDATE sintoma SET nome = %s WHERE id = %s", (nome, sintoma_id))
        if tratamento:
            cursor.execute("UPDATE sintoma SET tratamento = %s WHERE id = %s", (tratamento, sintoma_id))

        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Deletar Sintoma
def deletar_sintoma_no_bd(sintoma_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o sintoma existe
        cursor.execute("SELECT * FROM sintoma WHERE id = %s", (sintoma_id,))
        sintoma = cursor.fetchone()
        if not sintoma:
            raise HTTPException(status_code=404, detail="Sintoma não encontrado")

        # Deletar o sintoma
        cursor.execute("DELETE FROM sintoma WHERE id = %s", (sintoma_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()



#-------------------CRUD para Remedio------------------

# Criar Remedio
def criar_remedio(nome: str, data_fabricacao: date, data_validade: date, prescricao: str):
    connection = get_connection()
    cursor = connection.cursor()

    # tem que ser assim 2024-10-25

    cursor.execute("INSERT INTO remedio (nome, data_fabricacao, data_validade, prescricao) VALUES (%s, %s, %s, %s) RETURNING id", 
                   (nome, data_fabricacao, data_validade, prescricao))
    

    remedio_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return remedio_id

# Listar Remedios
def listar_remedios():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM remedio")
    remedios = cursor.fetchall()
    connection.close()
    return remedios

# Atualizar Remedio no banco de dados
def atualizar_remedio_no_bd(remedio_id: int, nome: str = None, data_fabricacao: date = None, data_validade: date = None, prescricao: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o remedio existe
        cursor.execute("SELECT * FROM remedio WHERE id = %s", (remedio_id,))
        remedio = cursor.fetchone()
        if not remedio:
            raise HTTPException(status_code=404, detail="Remedio não encontrado")

        # Atualizar os campos se houverem novos valores
        if nome:
            cursor.execute("UPDATE remedio SET nome = %s WHERE id = %s", (nome, remedio_id))
        if data_fabricacao:
            cursor.execute("UPDATE remedio SET data_fabricacao = %s WHERE id = %s", (data_fabricacao, remedio_id))
        if data_validade:
            cursor.execute("UPDATE remedio SET data_validade = %s WHERE id = %s", (data_validade, remedio_id))
        if prescricao:
            cursor.execute("UPDATE remedio SET prescricao = %s WHERE id = %s", (prescricao, remedio_id))

        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Deletar Remedio
def deletar_remedio_no_bd(remedio_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o remedio existe
        cursor.execute("SELECT * FROM remedio WHERE id = %s", (remedio_id,))
        remedio = cursor.fetchone()
        if not remedio:
            raise HTTPException(status_code=404, detail="Remedio não encontrado")

        # Deletar o remedio
        cursor.execute("DELETE FROM remedio WHERE id = %s", (remedio_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()



#-------------------CRUD para PacienteSintoma------------------

# Criar a associação de Sintoma com Paciente
def associar_sintoma_com_paciente(paciente_id: int, sintoma_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO paciente_sintoma (paciente_id, sintoma_id) VALUES (%s, %s) RETURNING paciente_id, sintoma_id", 
                   (paciente_id, sintoma_id))
    result = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return {"paciente_id": result[0], "sintoma_id": result[1]}

# Listar Sintomas associados a um paciente
def listar_sintomas_do_paciente(paciente_id: int):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM sintoma s JOIN paciente_sintoma ps ON s.id = ps.sintoma_id WHERE ps.paciente_id = %s", 
                   (paciente_id,))
    sintomas = cursor.fetchall()
    connection.close()
    return sintomas

# Deletar a associação de Sintoma com Paciente
def remover_associacao_paciente_sintoma(paciente_id: int, sintoma_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM paciente_sintoma WHERE paciente_id = %s AND sintoma_id = %s", 
                   (paciente_id, sintoma_id))
    connection.commit()
    cursor.close()
    connection.close()



#-------------------CRUD para Receita(medico-paciente-remedio)------------------

# Criar a receita (associar médico, remédio e paciente)
def criar_receita(medico_id: int, remedio_id: int, paciente_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO receita (medico_id, remedio_id, paciente_id) VALUES (%s, %s, %s) RETURNING medico_id, remedio_id, paciente_id", 
                   (medico_id, remedio_id, paciente_id))
    result = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return {"medico_id": result[0], "remedio_id": result[1], "paciente_id": result[2]}

# Listar receitas de um paciente
def listar_receitas_do_paciente(paciente_id: int):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM receita r "
                   "JOIN medico m ON r.medico_id = m.id "
                   "JOIN remedio rm ON r.remedio_id = rm.id "
                   "WHERE r.paciente_id = %s", 
                   (paciente_id,))
    receitas = cursor.fetchall()
    connection.close()
    return receitas

# Listar receitas de um médico
def listar_receitas_do_medico(medico_id: int):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM receita r "
                   "JOIN paciente p ON r.paciente_id = p.id "
                   "JOIN remedio rm ON r.remedio_id = rm.id "
                   "WHERE r.medico_id = %s", 
                   (medico_id,))
    receitas = cursor.fetchall()
    connection.close()
    return receitas

# Deletar a receita (associação entre médico, remédio e paciente)
def remover_receita(medico_id: int, remedio_id: int, paciente_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM receita WHERE medico_id = %s AND remedio_id = %s AND paciente_id = %s", 
                   (medico_id, remedio_id, paciente_id))
    connection.commit()
    cursor.close()
    connection.close()
