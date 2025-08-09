import React from "react";
import { Navigate } from 'react-router-dom';

class ProtectedRouter extends React.Component{

    render(){
        const token = localStorage.getItem('access_token')
        if (!token){
            return <Navigate to="/" replace />;
        }
        return this.props.children;
    }

}

export default ProtectedRouter;