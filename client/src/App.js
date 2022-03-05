import React, { useState } from 'react';
import {
  BrowserRouter,
  Switch,
  Route
} from 'react-router-dom';
import UserContext from './context/UserContext';
import Dashboard from './views/Dashboard';
import LoginRegView from './views/LoginRegView';
import Main from './views/Main';

function App() {
  const [ userInfo, setUserInfo ] = useState({})

  return (
    <div className="App">
      <UserContext.Provider value={{userInfo, setUserInfo}} >
        <BrowserRouter>
          <Main>
            <Switch>
              <Route path='/register'>
                <LoginRegView viewMode="register" />
              </Route>
              <Route path='/dashboard'>
                <Dashboard />
              </Route>
              <Route path='/'>
                <LoginRegView viewMode="login" />
              </Route>
            </Switch>
          </Main>
        </BrowserRouter>
      </UserContext.Provider>
    </div>
  );
}

export default App;
