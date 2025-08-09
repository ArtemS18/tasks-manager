import { Form, Input, Button, Alert, message } from 'antd';
import React, { useState } from "react";
import { api } from "../../fetch/api.jsx";
import "./AuthoForm.css"

function AuthoForm(props) {
    const {handleError, handleSuccess, state, setState} = props

    const onFinish = async (values) => {
        try {
            const resp = await api.fetchAuthoData(values.username, values.password);
            resp.success ? handleSuccess(resp.access_token) : handleError(resp.message);
        } catch (e) {
            console.log(e)
            handleError({ detail: "Ошибка сервера или сети." });
        }
    };

    const onFinishFailed = (errorInfo) => {
        message.error("Ошибка заполнения формы");
        console.log('Validation Failed:', errorInfo);
    };

    return (
        <div className='container'>

            <Form
                className="autho-form"
                layout="vertical"
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
            >
                <h1 className='title'><strong>Войти в аккаунт</strong> </h1>
                <Form.Item
                    label="Имя пользователя"
                    name="username"
                    rules={[{ required: true, message: 'Введите имя пользователя!' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    label="Пароль"
                    name="password"
                    rules={[{ required: true, message: 'Введите пароль!' }]}
                >
                    <Input.Password />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" disabled={state.isSuccess} block>
                        Войти
                    </Button>
                </Form.Item>

            {state.isSuccess && (
                <Alert
                    message="Вы вошли!"
                    type="success"
                    showIcon
                    style={{ marginBottom: 16 }}
                />
            )}

            {state.isError && (
                <Alert
                    message="Ошибка авторизации"
                    description={state.errorDetails}
                    type="error"
                    showIcon
                    closable
                    onClose={() => setState({'isError': false})}
                    style={{ marginBottom: 16 }}
                />
            )}
            </Form>
        </div>
    );
}

export default AuthoForm;
