import logo from '../logo.svg';
import { GoogleLogin } from '@react-oauth/google';
import React from "react";
import axiosInstance from "./api";

function parseJwt (token) {
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

 return JSON.parse(jsonPayload);
};

function Login(props) {

  const responseMessage = async (response) => {
    const user = parseJwt(response.credential);
    const credential = response.credential;
    console.log(response.credential);

    try {
      const res = await axiosInstance.post(`/login/${user.sub}`);

      if (res.status === 200) {
        // Login successful
        props.onLogin(user, credential);
      } else {
        // Handle login error
        console.log('Login failed');
      }
    } catch (error) {
      console.log(error);
    }
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
