import logo from '../logo.svg';
import '../App.css';
import { GoogleLogin } from '@react-oauth/google';

function Login() {
  const responseMessage = (response) => {
      console.log(response);
  };
  const errorMessage = (error) => {
      console.log(error);
  };
  return (
    <div className="App">
      <header className="Login-header">
          <h2>MateoMonedas</h2>
            <br />
            <br />
          <GoogleLogin onSuccess={responseMessage} onError={errorMessage} />
        <img src={logo} className="App-logo" alt="logo" />
      </header>
    </div>
  );
}

export default Login;
