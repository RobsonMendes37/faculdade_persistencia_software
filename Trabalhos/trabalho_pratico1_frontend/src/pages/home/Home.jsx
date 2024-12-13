import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="container" id="homePage">
      <h2 className="title">Welcome to Supplier Management System</h2>
      <p className="subtitle">Find the best suppliers for your business.</p>
      <Link to="/produtos" className="btn btn-light" id="button_home">Ver Produtos</Link>
    </div>
  );
}

export default Home;
