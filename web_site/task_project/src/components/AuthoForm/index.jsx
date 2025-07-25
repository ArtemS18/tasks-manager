import { Form, Input, Button, Alert } from 'antd';
import { React, useState, } from "react"
import { api } from "../../fetch/api.jsx"

function AuthoForm() {
    const [isAutho, setStatusAuth] = useState(false)
    const [token, setToken] = useState(null)
    const [error, setError] = useState([])
    const [isError, setIsError] = useState(false)

    async function onFinish(values){
        const resp = await api.fetchAuthoData(values.username, values.password)
        if (resp.success){
            setStatusAuth(true)
            setIsError(false)
            setToken(resp.access_token)
            console.log(resp.access_token)
        }
        else{
            setStatusAuth(false)
            const msg = resp.message;  
            if (Array.isArray(msg.detail)) {
                setError(msg.detail.map(d=>d.msg).join("\n"))
                setIsError(true)
            } else if (msg.detail?.msg) {
                setError(msg.detail.msg);
                setIsError(true)
            } else if (typeof msg.detail == "string"){
                setError(msg.detail);
                setIsError(true)
            }else {
                setError(msg.detail);
                setIsError(true)
            }
        }
    };
    const onFinishFailed = errorInfo => {
        console.log('Failed:', errorInfo);
        message.error(errorInfo)
    };

    return (
        <>
        {isAutho && (
            <Alert 
            message="Вы вошли!"
            type="success"
            description={token}
            />
        )}
        {isError && (
                <Alert
                    message="Ошибка авторизации"
                    description={error}
                    type="error"
                    showIcon
                    closable
                    style={{ marginBottom: 16 }}
                    onClose={()=>setIsError(false)}
                />
        )}
        <Form
        name="basic"
        initialValues={{ remember: true }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off">
        <Form.Item
        label="Username"
        name="username"
        rules={[{ required: true, message: 'Please input your username!' }]}
        >
            <Input />
        </Form.Item>

        <Form.Item
        label="Password"
        name="password"
        rules={[{ required: true, message: 'Please input your password!' }]}
        >
            <Input.Password />
        </Form.Item>
        <Form.Item label={null}>
            <Button type="primary" htmlType="submit">
                Submit
            </Button>
        </Form.Item>
    </Form>
    </>)
}



export default AuthoForm