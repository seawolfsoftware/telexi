import logo from './logo.svg';
import './App.css';
import React from 'react';
import Counter from './components/Counter';
import CounterHook from './components/CounterHook';





function App() {


  return (
    <div className="container">

      <Counter />
      <CounterHook />


    </div>
  );
}

export default App;
