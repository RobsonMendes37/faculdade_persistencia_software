from http.client import CREATED
from fastapi import APIRouter, HTTPException 
from app.models.produto import Produto
from app.logs.logger import enviar_log
from app.services.lerDadosCsv import ler_dados_csv
from app.services.escreverDadosCsv import escrever_dados_csv

crud_router = APIRouter()
csv_FILE = "app/database/database.csv"
#   "hash_sha256": "c01268ef42f8b74b2484f0bb519c76999ed4475a8b813ae3fde0f604ccfe762e"


# GET
@crud_router .get("/produtos", response_model=list[Produto])
def listar_produtos():
    try:
        enviar_log("Iniciando listagem de produtos por '/produtos'...") # Registrar no log antes de processar

        produtos = ler_dados_csv() # Chama a função que lê os dados do CSV

        # Sucesso: registra a operação no log
        enviar_log("Listagem de produtos por '/produtos' realizada com sucesso")
        return produtos
    
    except Exception as e:
        # Se ocorrer qualquer erro, captura e registra no log
        erro_msg = f"Erro ao listar produtos::  {str(e)}"
        enviar_log(erro_msg)
        
        # Lança uma exceção HTTP para retornar um erro adequado para o cliente
        raise HTTPException(status_code=500, detail="Erro interno em /produtos ao processar a requisição.")



# GET por ID
@crud_router .get("/produtos/{id}", response_model=Produto)
def get_products_by_id(id: int):
    try:
        enviar_log(f"Iniciando busca de produto por ID '{id}' em '/produtos/{id}'...")  # Log de início

        products = ler_dados_csv()  # Lê os dados do CSV

        for product in products:
            if product.id == id:
                enviar_log(f"Produto com ID '{id}' encontrado com sucesso em '/produtos/{id}'")  # Log de sucesso
                return product

        # Produto não encontrado
        enviar_log(f"Produto com ID '{id}' não encontrado em '/produtos/{id}'")
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    except Exception as e:
        # Captura e registra qualquer erro inesperado
        erro_msg = f"Erro ao buscar produto por ID '{id}' em '/produtos/{id}': {str(e)}"
        enviar_log(erro_msg)

        # Lança uma exceção HTTP para retornar um erro interno
        raise HTTPException(status_code=500, detail="Erro interno em /produtos/{id} ao processar a requisição.")





# POST
@crud_router.post("/produtos", response_model=Produto, status_code=201)
def criar_produto(produto: Produto):
    try:
        # Log de início
        enviar_log(f"Iniciando criação de produto com ID '{produto.id}' em '/produtos'...") 

        enviar_log(f"Dados recebidos para criação de produto: {produto}")
        enviar_log(f"Tipo de produto.id: {type(produto.id)}")
        enviar_log(f"Tipo de produto.nome: {type(produto.nome)}")
        enviar_log(f"Tipo de produto.tipo: {type(produto.tipo)}")
        enviar_log(f"Tipo de produto.peso: {type(produto.peso)}")
        enviar_log(f"Tipo de produto.tamanho: {type(produto.tamanho)}")
        enviar_log(f"Tipo de produto.preco: {type(produto.preco)}")
        enviar_log(f"Tipo de produto.quantidade: {type(produto.quantidade)}")
        enviar_log(f"Tipo de produto.fornecedor: {type(produto.fornecedor)}")
        enviar_log(f"Tipo de produto.marca: {type(produto.marca)}")


        produtos = ler_dados_csv()  # Lê os dados do CSV



        # Verifica se o produto já existe
        for p in produtos:
            if p.id == produto.id:
                enviar_log(f"Falha ao criar produto: Produto com ID '{produto.id}' já existe em '/produtos'")
                raise HTTPException(status_code=400, detail="Produto já existe")

        # Adiciona o novo produto
        produtos.append(produto)
        escrever_dados_csv(produtos)  # Escreve os dados atualizados no CSV

        enviar_log(f"Produto com ID '{produto.id}' criado com sucesso em '/produtos'")  # Log de sucesso
        return produto

    except HTTPException as http_ex:
        # Repassa a exceção HTTP sem registrar novamente (já registrada acima)
        raise http_ex

    except Exception as e:
        # Captura e registra qualquer erro inesperado
        erro_msg = f"Erro ao criar produto com ID '{produto.id}' em '/produtos': {str(e)}"
        enviar_log(erro_msg)
        
        # Lança uma exceção HTTP para retornar um erro interno
        raise HTTPException(status_code=500, detail="Erro interno em /produtos ao processar a requisição.")





# PUT
@crud_router .put("/produtos/{id}", response_model=Produto)
def atualizar_produto(id: int, produtoAtualizado: Produto):
    try:
        enviar_log(f"Iniciando atualização do produto com ID '{id}' em '/produtos'...")  # Log de início

        produtos = ler_dados_csv()  # Lê os dados do CSV

        # Busca pelo produto com o ID fornecido
        for i, produto in enumerate(produtos):
            if produto.id == id:
                produtos[i] = produtoAtualizado  # Atualiza o produto
                escrever_dados_csv(produtos)  # Escreve os dados atualizados no CSV
                
                enviar_log(f"Produto com ID '{id}' atualizado com sucesso em '/produtos'")  # Log de sucesso
                return produtoAtualizado
        
        # Se o produto não for encontrado
        enviar_log(f"Falha ao atualizar produto: Produto com ID '{id}' não encontrado em '/produtos'")
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    except HTTPException as http_ex:
        # Repassa a exceção HTTP sem registrar novamente (já registrada acima)
        raise http_ex

    except Exception as e:
        # Captura e registra qualquer erro inesperado
        erro_msg = f"Erro ao atualizar produto com ID '{id}' em '/produtos': {str(e)}"
        enviar_log(erro_msg)
        
        # Lança uma exceção HTTP para retornar um erro interno
        raise HTTPException(status_code=500, detail="Erro interno em /produtos ao processar a requisição.")






# DELETE
@crud_router .delete("/produtos/{id}")
def remover_produto(id: int):
    try:
        enviar_log(f"Iniciando remoção do produto com ID '{id}' em '/produtos'...")  # Log de início

        produtos = ler_dados_csv()  # Lê os dados do CSV
        produtos_filtrados = [produto for produto in produtos if produto.id != id]  # Filtra o produto com o ID fornecido
        
        # Verifica se o produto foi encontrado
        if len(produtos) == len(produtos_filtrados):
            enviar_log(f"Falha ao remover produto: Produto com ID '{id}' não encontrado em '/produtos'")  # Log de falha
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        # Se o produto for encontrado, escreve os dados atualizados no CSV
        escrever_dados_csv(produtos_filtrados)
        
        # Registra o sucesso da operação
        enviar_log(f"Produto com ID '{id}' removido com sucesso em '/produtos'")  # Log de sucesso
        return {"message": "Produto deletado"}

    except Exception as e:
        # Captura e registra qualquer erro inesperado
        erro_msg = f"Erro ao remover produto com ID '{id}' em '/produtos': {str(e)}"
        enviar_log(erro_msg)
        
        # Lança uma exceção HTTP para retornar um erro interno
        raise HTTPException(status_code=500, detail="Erro interno em /produtos ao processar a requisição.")



