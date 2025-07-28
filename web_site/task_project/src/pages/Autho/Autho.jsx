import React from "react"
import AuthoForm from "../../components/AuthoForm/index.jsx"
import './Autho.css'
class Autho extends React.Component{
    render(){
        return <div className="autho-window"> 
            <AuthoForm/>
        </div>
    }

}

export default Autho