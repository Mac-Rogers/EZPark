import React from 'react';
import EntryForm from './components/EntryForm';
import MapComponent from './components/MapComponent';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <div className="content">
        <div className='Navbar'>
        <h1>EZPark</h1>
        <EntryForm />
        </div>
        <MapComponent />
      </div>
    </div>
  );
};

export default App;
