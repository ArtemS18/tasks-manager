import { Form, Input, Button, Alert, message } from 'antd';
import React, { useState } from "react";
import { api } from "../../fetch/api.jsx";
import "./RegisterForm.css"

function RegisterForm(props) {
    const {handleError, handleSuccess, state, setState} = props

    const onFinish = async (values) => {
        if (values.password !=values.repeate_password){
            handleError({ detail: "Пароли должны совпадать" });
            return
        }
        try {
            const resp = await api.fetchRegData(values.name, values.password, values.login);
            resp.success ? handleSuccess(resp.confirm_token) : handleError(resp.message);
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
                className="register-form"
                layout="vertical"
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
            >
                <h1 className='title'><strong>Регистрация</strong> </h1>
                <Form.Item
                    label="Имя пользователя"
                    name="name"
                    rules={[{ required: true, message: 'Введите имя пользователя!' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    label="Почта"
                    name="login"
                    rules={[{ required: true, message: 'Введите почту!' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    label="Придумайте пароль"
                    name="password"
                    rules={[{ required: true, message: 'Введите пароль!' }]}
                >
                    <Input.Password />
                </Form.Item>

                <Form.Item
                    label="Повторите пароль"
                    name="repeate_password"
                    rules={[{ required: true, message: 'Повторите пароль!' }]}
                >
                    <Input.Password />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" disabled={state.isSuccess} block>
                        Зарегистрироваться
                    </Button>
                </Form.Item>

            {state.isSuccess && (
                <Alert
                    message="Вы зарегистрировались!"
                    type="success"
                    showIcon
                    style={{ marginBottom: 16 }}
                />
            )}

            {state.isError && (
                <Alert
                    message="Ошибка регистрации"
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

export default RegisterForm;
