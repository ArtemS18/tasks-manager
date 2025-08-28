import React from "react"
import './Register.css'
import RegisterForm from "../../components/RegisterForm/RegisterForm.jsx"
import { Navigate } from "react-router-dom"
class RegisterPage extends React.Component{
    constructor(props){
        super(props)
        this.state ={
            'confirmToken':null, 
            'errorDetails': "", 
            'isError': false,
            'isSuccess':false,
            'redirect': false 

        }
    }
    handleSuccess = async (confirmToken) => {
        localStorage.setItem("confirm_token", confirmToken);
        console.log(confirmToken)
        this.setState({ 
            'confirmToken': confirmToken, 
            'isSuccess': true, 
            'isError': false,
            'redirect': true 
        });
        //this.props.navigate("/confirm"); 
        //message.success("Успешный вход!");
    };

    handleError = (msg) => {
        let errorMsg = "Неизвестная ошибка";
        let detail;
        if (typeof msg === "string"){
            detail = msg;
        }else if (msg?.detail){
            detail = msg.detail;
        }
        if (Array.isArray(detail)) {
            errorMsg = detail.map(d => d.msg).join("\n");
        } else if (typeof detail === "object" && detail?.msg) {
            errorMsg = detail.msg;
        } else if (typeof detail === "string") {
            errorMsg = detail;
        }

        this.setState({ 
            'errorDetails': errorMsg, 
            'isError': true
        });
    };

    render(){
        if (this.state.redirect){
            return <Navigate 
                to="/confirm"
                replace 
                state={{ confirmToken: this.state.confirmToken }} />;
        }
        return<>
            <div className="register-window"> 
                <RegisterForm 
                handleError={this.handleError} 
                handleSuccess={this.handleSuccess} 
                state={this.state}
                setState={this.setState.bind(this)}/>
                
            </div>
        </>
        
    }

}

export default  RegisterPage