import { useEffect, useState } from 'react';
import './App.css';
import TaskCard from './components/TaskCard/index.jsx';
import Autho from './pages/Autho/Autho.jsx'
import axios from 'axios';
import warning from 'antd/es/_util/warning.js';

function App() {
  return (
    <div>
      <h1 className="text-3xl font-bold"> Your tasks </h1>
      <Autho></Autho>
    </div>
  )
}

export default App
