import logo from '../logo.svg';
import { GoogleLogin } from '@react-oauth/google';

function parseJwt (token) {
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

 return JSON.parse(jsonPayload);
};

function Login(props) {

  const responseMessage = (response) => {
    const user = parseJwt(response.credential);
    props.onLogin(user);
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
