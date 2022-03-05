import React, {useContext} from 'react';
import { useHistory } from 'react-router-dom';
import UserService from '../../services/UserService';
import UserContext from '../../context/UserContext';

const Logout = () => {
    const history = useHistory();
    const userContext = useContext(UserContext);

    const handleLogout = () => {
        UserService.logoutUser()
        .then(res=>{
            console.log(res.data)
            if(res.data.logout) {
                history.push('/');
                userContext.setUserInfo(null);
            }
        })
    }

    return (
        <div>
            <button onClick={handleLogout} >Logout</button>
        </div>
    )
}

export default Logout;