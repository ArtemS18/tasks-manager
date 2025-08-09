import React from "react"
import { Form, Input, Button, Alert } from 'antd';
import { Navigate, useLocation} from "react-router-dom"
import { api } from "../../fetch/api.jsx";
import './ConfirmPage.css'
class ConfirmPage extends React.Component{
    constructor(props){
        super(props)
        this.state ={
            'errorDetails': "", 
            'isError': false,
            'isSuccess':false,
            'redirect': false 

        }
    }
    onFinish = async (values) => {
        try {
            const confirmToken = this.props.location.state?.confirmToken;
            console.log(this.props.confirm_token, values.password)
            const resp = await api.fetchConfirmData(confirmToken, values.password);
            resp.success ? this.handleSuccess() : this.handleError(resp.message);
        } catch (e) {
            console.log(e)
            this.handleError({ detail: "Ошибка сервера или сети." });
        }
    };

    onFinishFailed = (errorInfo) => {
        console.log('Validation Failed:', errorInfo);
    };
    handleSuccess = async () => {
        this.setState({ 
            'isSuccess': true, 
            'isError': false,
            'redirect': true 
        });
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
            return <Navigate to="/success" replace />;
        }
        return<>
            <div className="confirm-window"> 
                <Form
                    className="confirm-form"
                    layout="vertical"
                    initialValues={{ remember: true }}
                    onFinish={this.onFinish}
                    onFinishFailed={this.onFinishFailed}
                    autoComplete="off"
                >
                <h1 className='title'><strong>Подтвердите почту</strong> </h1>
                <Form.Item
                    label="Введите код"
                    name="password"
                    rules={[{ required: true, message: 'Введите код!' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" disabled={this.state.isSuccess} block>
                        Подтвердить
                    </Button>
                </Form.Item>

                {this.state.isSuccess && (
                                <Alert
                                    message="Вы вошли!"
                                    type="success"
                                    showIcon
                                    style={{ marginBottom: 16 }}
                                />
                )}
    
                {this.state.isError && (
                    <Alert
                        message="Ошибка авторизации"
                        description={this.state.errorDetails}
                        type="error"
                        showIcon
                        closable
                        onClose={() => setState({'isError': false})}
                        style={{ marginBottom: 16 }}
                    />
                )}
            </Form>
            </div>
        </>
        
    }

}

function withRouter(Component) {
    return function WrappedComponent(props) {
        const location = useLocation();
        return <Component {...props} location={location} />;
    };
}


export default withRouter(ConfirmPage);