import React from "react"
import { useNavigate } from "react-router-dom";
import { useSearchParams } from "react-router-dom";
import AuthoForm from "../../components/AuthoForm/index.jsx"
import './Autho.css'
import { api } from "../../fetch/api.jsx";
class AuthoPage extends React.Component{
    constructor(props){
        super(props)
        this.state ={
            'accessToken':null, 
            'errorDetails': "", 
            'isError': false,
            'isSuccess':false,

        }
    }
    handleSuccess = async (accessToken) => {
        localStorage.setItem("access_token", accessToken);
        const tgId = this.props.params.get("tg_id")
        if (!tgId){
            this.handleError("Отсутствует query-parametr: tg_id")
            return null
        }
        const res = await api.updateTgId(accessToken, tgId)
        console.log(res)
        if (!res.success){
            this.handleError("Ошибка авторизации tg")
            return null
        }
        this.setState({ 
            'accessToken': accessToken, 
            'isSuccess': true, 
            'isError': false
        });
        this.props.navigate("/success"); 
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
        return <div className="autho-window"> 
            <AuthoForm 
            handleError={this.handleError} 
            handleSuccess={this.handleSuccess} 
            state={this.state}
            setState={this.setState.bind(this)}/>
            
        </div>
    }

}

function AuthoPageWrapper(){
    const navigate = useNavigate()
    const [searchParams] = useSearchParams();
    return (
        <AuthoPage navigate={navigate} params={searchParams}/>
    )

}

export default AuthoPageWrapper