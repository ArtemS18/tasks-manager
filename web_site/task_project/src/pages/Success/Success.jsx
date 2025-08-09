import React from "react"
import { Alert} from 'antd';

class SuccessPage extends React.Component{
    render(){
        return <Alert
                    message="Вы вошли! Можете закрыть это окно"
                    type="success"
                    showIcon
                    style={{ marginBottom: 16, fontSize: '18px' }}
                />
    }
}

export default SuccessPage;