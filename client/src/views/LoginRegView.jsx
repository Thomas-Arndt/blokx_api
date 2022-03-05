import React from 'react';
import Login from '../components/LoginReg/Login';
import Register from '../components/LoginReg/Register';

const LoginRegView = ({ setUserInfo, viewMode }) => {
    return (
        <div className="d-flex flex-column align-items-center mt-5">
            {viewMode === "register" &&
                <Register setUserInfo={setUserInfo} />}
            {viewMode === "login" &&
                <Login setUserInfo={setUserInfo} />}
        </div>
    )
}

export default LoginRegView;