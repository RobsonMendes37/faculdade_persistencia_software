import Footer from './components/Footer/Footer';
import Header from './components/Header/Header';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/home/Home';
import AddProduto from './pages/addProduto/AddProduto';
import UpdateProduto from './pages/updateProduto/UpdateProduto';
import ListProdutos from './pages/listProdutos/ListProduto';
import ViewProduto from './pages/viewProduto/ViewProduto';

function App() {
  return (
    <>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/produtos" element={<ListProdutos />} />
          <Route path="/add-produto" element={<AddProduto />} />
          <Route path="/edit-produto/:id" element={<UpdateProduto />} />
          <Route path="/view-produto/:id" element={<ViewProduto />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;
