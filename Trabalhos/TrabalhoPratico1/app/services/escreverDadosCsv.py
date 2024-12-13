import csv
from app.models.produto import Produto
csv_FILE = "app/database/database.csv"


# Escrever os dados no CSV
def escrever_dados_csv(produtos):
    with open(csv_FILE, mode="w", newline="") as file:
        fieldnames = ["id", "nome", "tipo", "peso", "tamanho", "preco", "quantidade", "fornecedor", "marca"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            # Converte 'tipo' e 'tamanho' para string explicitamente, caso necessário
            produto_dict = produto.dict()
            produto_dict['tipo'] = str(produto.tipo)  # Certificando-se de que 'tipo' é string
            produto_dict['tamanho'] = str(produto.tamanho)  # Certificando-se de que 'tamanho' é string
            writer.writerow(produto_dict)