import axios from "axios";

const REST_API_BASE_URL = 'http://localhost:8000/produtos';

export const listProdutos = () =>  axios.get(REST_API_BASE_URL)

export const createProduto = (produto) => axios.post(REST_API_BASE_URL, produto);

export const getProduto = (produtoId) => axios.get(REST_API_BASE_URL + '/' + produtoId);

export const updateProduto = (produtoId , produto) => axios.put(REST_API_BASE_URL + '/' + produtoId,produto);

export const deleteProduto = (produtoId) => axios.delete(REST_API_BASE_URL + '/' + produtoId)

