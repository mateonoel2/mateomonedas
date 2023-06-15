import { useState } from 'react';
import './App.css';
import Login from './components/login';
import Account from './components/account';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState({});

  const handleLogin = (user) => {
    setIsLoggedIn(true);
    setUser(user);
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        <>
          <Account user={user} />
        </>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
