import React, { useState, useContext } from 'react';
import { useHistory } from 'react-router-dom';
import AxiosService from '../../services/AxiosService';
import UserContext from '../../context/UserContext'
import styles from './Login.module.css';

const Login = ({ setUserInfo }) => {
    const history = useHistory();
    const userContext = useContext(UserContext);
    const [ email, setEmail ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ errors, setErrors] = useState({})

    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = {
            email: email,
            password: password
        }
        AxiosService.getRestClient().post('/users/login', formData, {withCredentials: true})
            .then(res => {
                console.log(res.data)
                if(res.data.status === 400) {
                    let errorList = {};
                    for (const error in res.data.errors) {
                        errorList[error] = res.data.errors[error];
                    }
                    setErrors(errorList);
                } else {
                    userContext.setUserInfo(res.data.user)
                    history.push('/dashboard');
                }
            })
            .catch(err => console.log(err))
    }

    return (
        <div className={styles.wrapper}>
            <h2 className={styles.title}>Login</h2>
            <form onSubmit={handleSubmit} className={styles.form} >
                <input type="email"
                    name="email"
                    value={email}
                    onChange={(e)=>setEmail(e.target.value)}
                    placeholder="Email"
                    className={`form-control ${styles.inputBox}`} />
                <input type="password"
                    name="password"
                    value={password}
                    onChange={(e)=>setPassword(e.target.value)}
                    placeholder="Password"
                    className={`form-control ${styles.inputBox}`} />
                <input type="submit" value="Login" className={styles.submit} />
            </form>
            <p className='p-0 my-0 mt-3'>Not a member yet? <a href="/register">Register</a></p>
        </div>
    )
}

export default Login;