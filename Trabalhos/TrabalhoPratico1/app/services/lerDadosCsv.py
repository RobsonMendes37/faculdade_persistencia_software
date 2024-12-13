import csv
import os
from app.models.produto import Produto

csv_FILE = "app/database/database.csv"

def ler_dados_csv():
    produtos = []
    if os.path.exists(csv_FILE):
        with open(csv_FILE, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(Produto(**row))
    else:
        print("O arquivo não existe")
    return produtos
