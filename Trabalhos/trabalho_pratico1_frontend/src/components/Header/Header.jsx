import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <div>
      <header>
        <nav className='navbar navbar-expand-lg navbar-dark bg-dark'>
          <a className="navbar-brand ml-2" href='http://localhost:3000'>Supplier Management System</a> 
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <a className="nav-link" href='http://localhost:5173'>Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href='http://localhost:5173/produtos'>List of Suppliers</a>
              </li>
            </ul>
          </div>
        </nav>
      </header>
    </div>
  )
}

export default Header;
