import React, { useState } from 'react';
import './App.css';
import Login from './components/login';
import Account from './components/account';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState({});
  const [credential, setCredential] = useState();

  const handleLogin = (user, credential) => {
    setIsLoggedIn(true);
    setUser(user);
    setCredential(credential)
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        <>
          <Account user={user} credential={credential} />
        </>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
