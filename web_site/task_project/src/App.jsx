import './App.css';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import AuthoPageWrapper from './pages/Autho/Autho.jsx'
import SuccessPage from './pages/Success/Success.jsx'
import ProtectedRouter from './components/ProtectedRouter/ProtectedRouter.jsx';
import RegisterPage from './pages/Register/Register.jsx';
import ConfirmPage from './pages/Cofirm/ConfitmPage.jsx';
function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path='/tg_autho' element={<AuthoPageWrapper/>}/>
          <Route path='/reg' element={<RegisterPage/>} />
          <Route path='/confirm' element={<ConfirmPage/>}/>
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
