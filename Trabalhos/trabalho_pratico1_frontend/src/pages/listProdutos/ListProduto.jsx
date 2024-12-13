import React, { useState, useEffect } from 'react';
import { listProdutos, deleteProduto } from '../../services/ProdutoServicer';
import { useNavigate } from 'react-router-dom';
import './ListProduto.css';

const ListProdutos = () => {
  const [produtos, setProdutos] = useState([]);
  const navigator = useNavigate();

  useEffect(() => {
    getAllProdutos();
  }, []);

  function getAllProdutos() {
    listProdutos()
      .then((response) => {
        setProdutos(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }

   //Função de navegação para criar um novo produto (caso necessário)
   function addNewProduto() {
        navigator('/add-produto');
   }

  // Função de navegação para editar um produto (caso necessário)
  function updateProduto(id) {
    navigator(`/edit-produto/${id}`);
  }

  function removeProduto(id){
    console.log(id);

    deleteProduto(id).then((response) =>{
        getAllProdutos();
    }).catch(error => {
        console.error(error);
    })
}

  const viewProduto = (id) => {
    navigator(`/view-produto/${id}`);
};

  return (
    <div className="container">
      <h2 className="text-center" id="title">
        Lista de Produtos
      </h2>
      {/* Botão para adicionar um novo produto, se necessário */}
      <button className="btn btn-primary mb-2" onClick={addNewProduto}>Adicionar Produto</button> 
      <table className="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Id</th>
            <th>Nome</th>
            <th>Tipo</th>
            <th>Peso</th>
            <th>Tamanho</th>
            <th>Preço</th>
            <th>Quantidade</th>
            <th>Fornecedor</th>
            <th>Marca</th>
            {/* Colunas para ações como editar ou excluir, caso seja necessário */}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {
            produtos.map((produto) => (
              <tr key={produto.id}>
                <td>{produto.id}</td>
                <td>{produto.nome}</td>
                <td>{produto.tipo}</td>
                <td>{produto.peso}</td>
                <td>{produto.tamanho}</td>
                <td>{produto.preco}</td>
                <td>{produto.quantidade}</td>
                <td>{produto.fornecedor}</td>
                <td>{produto.marca}</td>
                {/* Coluna de ações (editar, excluir, etc.) */}
                 <td id="actions">
                  <button className="btn btn-success" onClick={() => updateProduto(produto.id)}>Update</button>
                  <button className="btn btn-danger" onClick={() => removeProduto(produto.id)}>Delete</button>
                  <button className="btn btn-info" onClick={() => viewProduto(produto.id)}>Info</button>
                </td> 
              </tr>
            ))
          }
        </tbody>
      </table>
    </div>
  );
};

export default ListProdutos;
