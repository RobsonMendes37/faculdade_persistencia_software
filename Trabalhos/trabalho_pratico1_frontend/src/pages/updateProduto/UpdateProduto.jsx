import { useState,useEffect} from 'react';
import { updateProduto , getProduto} from '../../services/ProdutoServicer';
import { useNavigate } from 'react-router-dom';
import './UpdateProduto.css';

const UpdateProduto = () => {
    // const { id } = useParams();
    const navigator = useNavigate();

    // Estado para armazenar os campos
    const [id, setId] = useState('');
    const [nome, setNome] = useState('');
    const [tipo, setTipo] = useState('');
    const [peso, setPeso] = useState('');
    const [tamanho, setTamanho] = useState('');
    const [preco, setPreco] = useState('');
    const [quantidade, setQuantidade] = useState('');
    const [fornecedor, setFornecedor] = useState('');
    const [marca, setMarca] = useState('');
    const [errorMessage, setErrorMessage] = useState('');


    // Estado para armazenar os erros de validação
    const [errors, setErrors] = useState({
        id:'',
        nome: '',
        tipo: '',
        peso: '',
        tamanho: '',
        preco: '',
        quantidade: '',
        fornecedor: '',
        marca: '',
    });

    // Função para buscar o produto existente
    useEffect(() => {
        if (id) {
            getProduto(id).then((response) => {
                const produto = response.data;
                setNome(produto.nome);
                setTipo(produto.tipo);
                setPeso(produto.peso);
                setTamanho(produto.tamanho);
                setPreco(produto.preco);
                setQuantidade(produto.quantidade);
                setFornecedor(produto.fornecedor);
                setMarca(produto.marca);
            }).catch((error) => {
                console.error("Erro ao buscar produto:", error);
            });
        }
    }, [id]);

    // Enviar requisição POST
    function UpdateProduto(e){
        e.preventDefault();

        const produto = {id,nome,tipo,peso, tamanho,preco, quantidade, fornecedor,marca}
        console.log(produto)

        // Log dos dados antes de enviar
        console.log('Dados enviados:', JSON.stringify(produto, null, 2));


        if(validateForm()){
            updateProduto(id, produto).then((response) => {
                console.log(response.data);
                navigator('/produtos');
            }).catch(error => {
                console.error(error);
            })
        }
    }

    // Função de validação do formulário
    const validateForm = () => {
        let valid = true;
        let errorsCopy = { ...errors };

        // if (!id.trim()) {
        //     errorsCopy.id = 'ID é obrigatório';
        //     valid = false;
        // } else {
        //     errorsCopy.id = '';
        // }

        // // Validação de campos obrigatórios e formato
        // if (!nome.trim()) {
        //     errorsCopy.nome = 'Nome é obrigatório';
        //     valid = false;
        // } else {
        //     errorsCopy.nome = '';
        // }

        // if (!tipo.trim()) {
        //     errorsCopy.tipo = 'Tipo é obrigatório';
        //     valid = false;
        // } else if (!['limpeza', 'beleza', 'saude', 'comida'].includes(tipo)) {
        //     errorsCopy.tipo = 'Tipo inválido';
        //     valid = false;
        // } else {
        //     errorsCopy.tipo = '';
        // }

        // if (!peso.trim()){
        //     errorsCopy.peso = 'Peso inválido';
        //     valid = false;
        // } else {
        //     errorsCopy.peso = '';
        // }

        // if (!tamanho.trim()) {
        //     errorsCopy.tamanho = 'Tamanho é obrigatório';
        //     valid = false;
        // } else if (!['muitoPequeno', 'pequeno', 'medio', 'grande', 'muitoGrande'].includes(tamanho)) {
        //     errorsCopy.tamanho = 'Tamanho inválido';
        //     valid = false;
        // } else {
        //     errorsCopy.tamanho = '';
        // }

        // if (!preco.trim()) {
        //     errorsCopy.preco = 'Preço inválido';
        //     valid = false;
        // } else {
        //     errorsCopy.preco = '';
        // }

        // if (!quantidade.trim() || isNaN(quantidade) || parseInt(quantidade) <= 0) {
        //     errorsCopy.quantidade = 'Quantidade inválida';
        //     valid = false;
        // } else {
        //     errorsCopy.quantidade = '';
        // }

        // if (!fornecedor.trim()) {
        //     errorsCopy.fornecedor = 'Fornecedor é obrigatório';
        //     valid = false;
        // } else {
        //     errorsCopy.fornecedor = '';
        // }

        // if (!marca.trim()) {
        //     errorsCopy.marca = 'Marca é obrigatória';
        //     valid = false;
        // } else {
        //     errorsCopy.marca = '';
        // }

        setErrors(errorsCopy);
        return valid;
    };

    // Título da página
    function pageTitle() {
        return <h2 className='text-center'>Atualizar Produto</h2>;
    }

    return (
        <div className='container'>
            <br /> <br />
            <div className='row'>
                {pageTitle()}
                <div className='card col-md-10 offset-md-1'>
                    <h2>Dados do Produto</h2>
                    <hr />
                    <div className='card-body'>
                        <form id="produtoForm">
                            <div className="line">
                                {/* Id */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Id:</label>
                                    <input
                                        type='text'
                                        placeholder='Digite o ID do produto'
                                        name='id'
                                        value={id}
                                        className={`form-control ${errors.id ? 'is-invalid' : ''}`}
                                        onChange={(e) => setId(e.target.value)}
                                    />
                                    {errors.id && <div className='invalid-feedback'>{errors.id}</div>}
                                </div>

                                {/* Nome */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Nome:</label>
                                    <input
                                        type='text'
                                        placeholder='Digite o nome do produto'
                                        name='nome'
                                        value={nome}
                                        className={`form-control ${errors.nome ? 'is-invalid' : ''}`}
                                        onChange={(e) => setNome(e.target.value)}
                                    />
                                    {errors.nome && <div className='invalid-feedback'>{errors.nome}</div>}
                                </div>

                                {/* Tipo */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Tipo:</label>
                                    <select
                                        name='tipo'
                                        value={tipo}
                                        className={`form-control ${errors.tipo ? 'is-invalid' : ''}`}
                                        onChange={(e) => setTipo(e.target.value)}
                                    >
                                        <option value=''>Selecione o tipo</option>
                                        <option value='limpeza'>Limpeza</option>
                                        <option value='beleza'>Beleza</option>
                                        <option value='saude'>Saúde</option>
                                        <option value='comida'>Comida</option>
                                    </select>
                                    {errors.tipo && <div className='invalid-feedback'>{errors.tipo}</div>}
                                </div>


                                {/* Peso */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Peso:</label>
                                    <input
                                        type='text'
                                        placeholder='Digite o peso do produto'
                                        name='peso'
                                        value={peso}
                                        className={`form-control ${errors.peso ? 'is-invalid' : ''}`}
                                        onChange={(e) => setPeso(e.target.value)}
                                    />
                                    {errors.peso && <div className='invalid-feedback'>{errors.peso}</div>}
                                </div>

                                {/* Tamanho */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Tamanho:</label>
                                    <select
                                        name='tamanho'
                                        value={tamanho}
                                        className={`form-control ${errors.tamanho ? 'is-invalid' : ''}`}
                                        onChange={(e) => setTamanho(e.target.value)}
                                    >
                                        <option value=''>Selecione o tamanho</option>
                                        <option value='muitoPequeno'>Muito Pequeno</option>
                                        <option value='pequeno'>Pequeno</option>
                                        <option value='medio'>Médio</option>
                                        <option value='grande'>Grande</option>
                                        <option value='muitoGrande'>Muito Grande</option>
                                    </select>
                                    {errors.tamanho && <div className='invalid-feedback'>{errors.tamanho}</div>}
                                </div>


                                {/* Preço */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Preço:</label>
                                    <input
                                        type='text'
                                        placeholder='Digite o preço do produto'
                                        name='preco'
                                        value={preco}
                                        className={`form-control ${errors.preco ? 'is-invalid' : ''}`}
                                        onChange={(e) => setPreco(e.target.value)}
                                    />
                                    {errors.preco && <div className='invalid-feedback'>{errors.preco}</div>}
                                </div>

                                {/* Quantidade */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Quantidade:</label>
                                    <input
                                        type='text'
                                        placeholder='Digite a quantidade'
                                        name='quantidade'
                                        value={quantidade}
                                        className={`form-control ${errors.quantidade ? 'is-invalid' : ''}`}
                                        onChange={(e) => setQuantidade(e.target.value)}
                                    />
                                    {errors.quantidade && <div className='invalid-feedback'>{errors.quantidade}</div>}
                                </div>

                                {/* Fornecedor */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Fornecedor:</label>
                                    <input
                                        type='text'
                                        placeholder='Digite o nome do fornecedor'
                                        name='fornecedor'
                                        value={fornecedor}
                                        className={`form-control ${errors.fornecedor ? 'is-invalid' : ''}`}
                                        onChange={(e) => setFornecedor(e.target.value)}
                                    />
                                    {errors.fornecedor && <div className='invalid-feedback'>{errors.fornecedor}</div>}
                                </div>

                                {/* Marca */}
                                <div className='form-group mb-2'>
                                    <label className='form-label'>Marca:</label>
                                    <input
                                        type='text'
                                        placeholder='Digite a marca do produto'
                                        name='marca'
                                        value={marca}
                                        className={`form-control ${errors.marca ? 'is-invalid' : ''}`}
                                        onChange={(e) => setMarca(e.target.value)}
                                    />
                                    {errors.marca && <div className='invalid-feedback'>{errors.marca}</div>}
                                </div>

                                {/* Botão de Salvar */}
                                <button
                                    className='btn btn-primary'
                                    type='submit'
                                    onClick={UpdateProduto}
                                >
                                    {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                                    Atualizar Produto
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default UpdateProduto;
