import React, { useState, useEffect } from 'react';
import { getProduto } from '../../services/ProdutoServicer';
import { useParams, useNavigate } from 'react-router-dom';

const ViewProduto = () => {
  const [produto, setProduto] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      getProduto(id)
        .then(response => {
          setProduto(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }, [id]);

  if (!produto) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container">
      <h2 className="text-center">Detalhes do Produto</h2>
      <div className="card col-md-8 offset-md-2">
        <div className="card-body">
          <p><strong>Id:</strong> {produto.id}</p>
          <p><strong>Nome:</strong> {produto.nome}</p>
          <p><strong>Tipo:</strong> {produto.tipo}</p>
          <p><strong>Peso:</strong> {produto.peso}</p>
          <p><strong>Tamanho:</strong> {produto.tamanho}</p>
          <p><strong>Preço:</strong> {produto.preco}</p>
          <p><strong>Quantidade:</strong> {produto.quantidade}</p>
          <p><strong>Fornecedor:</strong> {produto.fornecedor}</p>
          <p><strong>Marca:</strong> {produto.marca}</p>

          <button className="btn btn-primary" onClick={() => navigate('/produtos')}>
            Voltar pra listagem
          </button>
        </div>
      </div>
    </div>
  );
};

export default ViewProduto;
