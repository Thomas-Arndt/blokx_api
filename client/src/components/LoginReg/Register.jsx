import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import styles from './Register.module.css';

const Register = () => {
    const history = useHistory();
    const [ firstName, setFirstName ] = useState('');
    const [ lastName, setLastName ] = useState('');
    const [ email, setEmail ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ confirmPassword, setConfirmPassword ] = useState('');
    const [ errors, setErrors ] = useState({});

    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            confirm_password: confirmPassword
        }
        axios.post('http://localhost:5000/api/createUser', formData, {withCredentials: true})
            .then(res=>{
                console.log(res.data)
                if(res.data.status === 400) {
                    let errorList = {};
                    for (const error in res.data.errors) {
                        errorList[error] = res.data.errors[error];
                    }
                    setErrors(errorList);
                } else {
                    history.push('/');
                }
            })
            .catch(err=>console.log(err))
    }

    const clearForm = () => {
        setFirstName("");
        setLastName("");
        setEmail("");
        setPassword("");
        setConfirmPassword("");
    }

    return (
        <div className={styles.wrapper}>
            <h2 className={styles.title}>Register</h2>
            <form onSubmit={handleSubmit} className={styles.form}>
                <input type="text"
                    name="firstName"
                    value={firstName}
                    onChange={(e)=>setFirstName(e.target.value)}
                    placeholder="First Name"
                    className={`form-control ${styles.inputBox}`} />
                <input type="text"
                    name="lastName"
                    value={lastName}
                    onChange={(e)=>setLastName(e.target.value)}
                    placeholder="Last Name"
                    className={`form-control ${styles.inputBox}`} />
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
                <input type="password"
                    name="confirmPassword"
                    value={confirmPassword}
                    onChange={(e)=>setConfirmPassword(e.target.value)}
                    placeholder="Retype Password"
                    className={`form-control ${styles.inputBox}`} />
                <input type="submit" 
                    value="Register"
                    className={`btn btn-warning ${styles.submit}`} />
            </form>
            <p className='p-0 my-0 mt-3'>Already registered? <a href="/">Login</a></p>
        </div>
    )
}

export default Register;