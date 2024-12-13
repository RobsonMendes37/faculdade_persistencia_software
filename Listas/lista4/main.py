from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xml.etree.ElementTree as ET
import os

app = FastAPI()
xml_FILE = "livros.xml"

# Modelo de dados para Livro
class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str

# Função para ler os dados do XML
def ler_dados_xml():
    livros = []
    if os.path.exists(xml_FILE):
        tree = ET.parse(xml_FILE)
        root = tree.getroot()
        for livro_element in root.findall("livro"):
            livro = Livro(
                id=int(livro_element.find("id").text),
                titulo=livro_element.find("titulo").text,
                autor=livro_element.find("autor").text,
                ano=int(livro_element.find("ano").text),
                genero=livro_element.find("genero").text,
            )
            livros.append(livro)
    else:
        print("O arquivo não existe")
    return livros

# Função para escrever os dados no XML
def escrever_dados_xml(livros):
    root = ET.Element("livros")
    for livro in livros:
        livro_element = ET.SubElement(root, "livro")
        ET.SubElement(livro_element, "id").text = str(livro.id)
        ET.SubElement(livro_element, "titulo").text = livro.titulo
        ET.SubElement(livro_element, "autor").text = livro.autor
        ET.SubElement(livro_element, "ano").text = str(livro.ano)
        ET.SubElement(livro_element, "genero").text = livro.genero

    tree = ET.ElementTree(root)
    tree.write(xml_FILE)

# Rota GET - Listar todos os livros
@app.get("/livros", response_model=list[Livro])
def listar_livros():
    return ler_dados_xml()

# Rota GET - Buscar livro por ID
@app.get("/livros/{id}", response_model=Livro)
def get_livro_by_id(id: int):
    livros = ler_dados_xml()
    for livro in livros:
        if livro.id == id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# Rota POST - Criar novo livro
@app.post("/livros", response_model=Livro, status_code=201)
def criar_livro(livro: Livro):
    livros = ler_dados_xml()
    for l in livros:
        if l.id == livro.id:
            raise HTTPException(status_code=400, detail="Livro já existe")

    livros.append(livro)
    escrever_dados_xml(livros)
    return livro

# Rota PUT - Atualizar livro por ID
@app.put("/livros/{id}", response_model=Livro)
def atualizar_livro(id: int, livro_atualizado: Livro):
    livros = ler_dados_xml()
    for i, livro in enumerate(livros):
        if livro.id == id:
            livros[i] = livro_atualizado
            escrever_dados_xml(livros)
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# Rota DELETE - Remover livro por ID
@app.delete("/livros/{id}")
def remover_livro(id: int):
    livros = ler_dados_xml()
    livros_filtrados = [livro for livro in livros if livro.id != id]
    if len(livros) == len(livros_filtrados):
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    escrever_dados_xml(livros_filtrados)
    return {"message": "Livro deletado"}

