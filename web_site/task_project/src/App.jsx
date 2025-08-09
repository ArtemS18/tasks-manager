import './App.css';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import AuthoPageWrapper from './pages/Autho/Autho.jsx'
import SuccessPage from './pages/Success/Success.jsx'
import ProtectedRouter from './components/ProtectedRouter/ProtectedRouter.jsx';
function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<AuthoPageWrapper/>}/>
          <Route path='/success' element={
            <ProtectedRouter>
              <SuccessPage />
            </ProtectedRouter>
          } />
        </Routes> 
      </BrowserRouter>
  )
}

export default App
