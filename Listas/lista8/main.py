from datetime import date
from fastapi import FastAPI, HTTPException
from crud import associar_sintoma_com_paciente, atualizar_medico_no_bd, atualizar_paciente_no_bd, atualizar_remedio_no_bd, atualizar_sintoma_no_bd, criar_medico,criar_paciente, criar_receita, criar_remedio, criar_sintoma, deletar_medico_no_bd, deletar_paciente_no_bd, deletar_remedio_no_bd, deletar_sintoma_no_bd, listar_medicos, listar_pacientes, listar_receitas_do_medico, listar_receitas_do_paciente, listar_remedios, listar_sintomas, listar_sintomas_do_paciente, remover_associacao_paciente_sintoma, remover_receita
from db import create_tables, get_connection
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Criação das tabelas no banco
create_tables()


#-----------------ENDPOITS PACIENTE------------------
#POST_paciente
@app.post("/pacientes/")
def criar_paciente_endpoint(nome: str, idade: int):
    paciente_id = criar_paciente(nome, idade)
    return {"id": paciente_id, "nome": nome, "idade": idade}

#GET_pacientes
@app.get("/pacientes/")
def listar_pacientes_endpoint():
    return listar_pacientes()

#PUT_paciente
@app.put("/pacientes/{paciente_id}/")
def atualizar_paciente_endpoint(paciente_id: int, nome: str = None, idade: int = None):
    try:
        # Chama a função que faz a atualização no banco de dados
        atualizar_paciente_no_bd(paciente_id, nome, idade)
        return {"message": "Paciente atualizado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

#DELETE_paciente
@app.delete("/pacientes/{paciente_id}/")
def deletar_paciente_endpoint(paciente_id: int):
    try:
        # Chama a função que faz a deleção no banco de dados
        deletar_paciente_no_bd(paciente_id)
        return {"message": "Paciente deletado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


#-----------------------ENDPOINTS MÉDICO----------------------

# POST Médico
@app.post("/medicos/")
def criar_medico_endpoint(nome: str, idade: int):
    try:
        medico_id = criar_medico(nome, idade)
        return {"id": medico_id, "nome": nome, "idade": idade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar médico: {str(e)}")

# GET Médicos
@app.get("/medicos/")
def listar_medicos_endpoint():
    try:
        return listar_medicos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar médicos: {str(e)}")

# PUT Médico
@app.put("/medicos/{medico_id}/")
def atualizar_medico_endpoint(medico_id: int, nome: str = None, idade: int = None):
    try:
        # Chama a função que faz a atualização no banco de dados
        atualizar_medico_no_bd(medico_id, nome, idade)
        return {"message": "Médico atualizado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# DELETE Médico
@app.delete("/medicos/{medico_id}/")
def deletar_medico_endpoint(medico_id: int):
    try:
        # Chama a função que faz a deleção no banco de dados
        deletar_medico_no_bd(medico_id)
        return {"message": "Médico deletado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


#-----------------ENDPOINTS SINTOMA------------------

# POST Sintoma
@app.post("/sintomas/")
def criar_sintoma_endpoint(nome: str, tratamento: str):
    try:
        sintoma_id = criar_sintoma(nome, tratamento)
        return {"id": sintoma_id, "nome": nome, "tratamento": tratamento}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar sintoma: {str(e)}")

# GET Sintomas
@app.get("/sintomas/")
def listar_sintomas_endpoint():
    try:
        return listar_sintomas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar sintomas: {str(e)}")

# PUT Sintoma
@app.put("/sintomas/{sintoma_id}/")
def atualizar_sintoma_endpoint(sintoma_id: int, nome: str = None, tratamento: str = None):
    try:
        # Chama a função que faz a atualização no banco de dados
        atualizar_sintoma_no_bd(sintoma_id, nome, tratamento)
        return {"message": "Sintoma atualizado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# DELETE Sintoma
@app.delete("/sintomas/{sintoma_id}/")
def deletar_sintoma_endpoint(sintoma_id: int):
    try:
        # Chama a função que faz a deleção no banco de dados
        deletar_sintoma_no_bd(sintoma_id)
        return {"message": "Sintoma deletado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")





#-----------------ENDPOINTS REMEDIO------------------

# POST Remedio
@app.post("/remedios/")
def criar_remedio_endpoint(nome: str, data_fabricacao: date, data_validade: date, prescricao: str):
    try:
        remedio_id = criar_remedio(nome, data_fabricacao, data_validade, prescricao)
        return {"id": remedio_id, "nome": nome, "data_fabricacao": data_fabricacao, "data_validade": data_validade, "prescricao": prescricao}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar remedio: {str(e)}")

# GET Remedios
@app.get("/remedios/")
def listar_remedios_endpoint():
    try:
        return listar_remedios()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar remedios: {str(e)}")

# PUT Remedio
@app.put("/remedios/{remedio_id}/")
def atualizar_remedio_endpoint(remedio_id: int, nome: str = None, data_fabricacao: date = None, data_validade: date = None, prescricao: str = None):
    try:
        # Chama a função que faz a atualização no banco de dados
        atualizar_remedio_no_bd(remedio_id, nome, data_fabricacao, data_validade, prescricao)
        return {"message": "Remedio atualizado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# DELETE Remedio
@app.delete("/remedios/{remedio_id}/")
def deletar_remedio_endpoint(remedio_id: int):
    try:
        # Chama a função que faz a deleção no banco de dados
        deletar_remedio_no_bd(remedio_id)
        return {"message": "Remedio deletado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


#-----------------ENDPOINTS PACIENTE-SINTOMA------------------

# POST - Associar Sintoma com Paciente
@app.post("/pacientes/{paciente_id}/sintomas/{sintoma_id}/")
def associar_sintoma_endpoint(paciente_id: int, sintoma_id: int):
    try:
        resultado = associar_sintoma_com_paciente(paciente_id, sintoma_id)
        return {"message": f"Sintoma {sintoma_id} associado ao paciente {paciente_id} com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao associar sintoma: {str(e)}")

# GET - Listar Sintomas de um Paciente
@app.get("/pacientes/{paciente_id}/sintomas/")
def listar_sintomas_do_paciente_endpoint(paciente_id: int):
    try:
        sintomas = listar_sintomas_do_paciente(paciente_id)
        return sintomas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar sintomas: {str(e)}")

# DELETE - Remover a associação de Sintoma com Paciente
@app.delete("/pacientes/{paciente_id}/sintomas/{sintoma_id}/")
def remover_associacao_endpoint(paciente_id: int, sintoma_id: int):
    try:
        remover_associacao_paciente_sintoma(paciente_id, sintoma_id)
        return {"message": f"Associação do sintoma {sintoma_id} com o paciente {paciente_id} removida com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover associação: {str(e)}")



#-----------------ENDPOINTS RECEITA------------------

# POST - Criar Receita (associar médico, remédio e paciente)
@app.post("/receitas/")
def criar_receita_endpoint(medico_id: int, remedio_id: int, paciente_id: int):
    try:
        resultado = criar_receita(medico_id, remedio_id, paciente_id)
        return {"message": "Receita criada com sucesso", "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar receita: {str(e)}")

# GET - Listar Receitas de um Paciente
@app.get("/pacientes/{paciente_id}/receitas/")
def listar_receitas_do_paciente_endpoint(paciente_id: int):
    try:
        receitas = listar_receitas_do_paciente(paciente_id)
        return receitas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar receitas: {str(e)}")

# GET - Listar Receitas de um Médico
@app.get("/medicos/{medico_id}/receitas/")
def listar_receitas_do_medico_endpoint(medico_id: int):
    try:
        receitas = listar_receitas_do_medico(medico_id)
        return receitas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar receitas: {str(e)}")

# DELETE - Remover Receita
@app.delete("/receitas/")
def remover_receita_endpoint(medico_id: int, remedio_id: int, paciente_id: int):
    try:
        remover_receita(medico_id, remedio_id, paciente_id)
        return {"message": "Receita removida com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover receita: {str(e)}")




#--------------------ENDPOITS com consultas complicadas-------------

# Endpoint para listar pacientes com a quantidade de sintomas
@app.get("/pacientes/sintomas/")
def listar_pacientes_com_sintomas():
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT p.id, p.nome, COUNT(ps.sintoma_id) AS numero_de_sintomas
            FROM paciente p
            LEFT JOIN paciente_sintoma ps ON p.id = ps.paciente_id
            GROUP BY p.id
            ORDER BY numero_de_sintomas DESC
        """)
        pacientes_com_sintomas = cursor.fetchall()
        connection.close()
        return pacientes_com_sintomas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pacientes com sintomas: {str(e)}")


# Endpoint para listar médicos com a quantidade de receitas prescritas
@app.get("/medicos/receitas/")
def listar_medicos_com_receitas():
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT m.id, m.nome, COUNT(r.id) AS numero_de_receitas
            FROM medico m
            LEFT JOIN receita r ON m.id = r.medico_id
            GROUP BY m.id
            ORDER BY numero_de_receitas DESC
        """)
        medicos_com_receitas = cursor.fetchall()
        connection.close()
        return medicos_com_receitas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar médicos com receitas: {str(e)}")


# Endpoint para listar remédios mais prescritos
@app.get("/remedios/mais-prescritos/")
def listar_remedios_mais_prescritos():
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT rm.id, rm.nome, COUNT(r.id) AS quantidade_prescricoes
            FROM remedio rm
            JOIN receita r ON rm.id = r.remedio_id
            GROUP BY rm.id
            HAVING COUNT(r.id) > 5
            ORDER BY quantidade_prescricoes DESC
        """)
        remedios_mais_prescritos = cursor.fetchall()
        connection.close()
        return remedios_mais_prescritos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar remédios mais prescritos: {str(e)}")


# Endpoint para listar sintomas mais comuns entre os pacientes
@app.get("/sintomas/comum/")
def listar_sintomas_comum():
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT s.id, s.nome, COUNT(ps.paciente_id) AS quantidade_de_pacientes
            FROM sintoma s
            JOIN paciente_sintoma ps ON s.id = ps.sintoma_id
            GROUP BY s.id
            ORDER BY quantidade_de_pacientes DESC
        """)
        sintomas_comuns = cursor.fetchall()
        connection.close()
        return sintomas_comuns
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar sintomas comuns: {str(e)}")
