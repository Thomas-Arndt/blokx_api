import React, { useContext } from 'react';
import Logout from '../components/Buttons/Logout';
import UserContext from '../context/UserContext';

const Dashboard = () => {
    const userContext = useContext(UserContext);
    return (
        <div>
            <h1>Welcome {userContext.userInfo.first_name}</h1>
            <Logout />
        </div>
    )
}

export default Dashboard;