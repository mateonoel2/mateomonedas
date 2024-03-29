import React, { useState, useEffect } from 'react';
import '../style/account.css';
import Miner from './miner';
import Transaction from './transaction';
import HandleAccount from './HandleAccount';
import axiosInstance from './api.js';

function Account({ user,  credential }) {
  const [public_key, setPublicKey] = useState();
  const [balance, setBalance] = useState();
  const [hasAccount, setAccount] = useState(false);

  useEffect(() => {

    const fetchPublicKey = async () => {
      try {
        var data = {"credential": credential};
        const response = await axiosInstance.post(`/public_key/${user.sub}`, data);
        const publicKey = await response.data;
        setPublicKey(publicKey);
        setAccount(true);
      } catch (error) {
        console.error('Error fetching public key:', error);
        setPublicKey("No public key found");
        setAccount(false);
      }
    };

    const fetchBalance = async () => {
      try {
        const response = await axiosInstance.get(`/balance/${user.sub}`);
        const balance_resp = await response.data;
        setBalance(balance_resp);
      } catch (error) {
        console.error('Error fetching balance:', error);
        setBalance("No balance found");
      }
    };
    
    fetchPublicKey();
    fetchBalance();
  }, [user.sub, credential]);

  const handleCopyPublicKey = () => {
    navigator.clipboard.writeText(public_key);
  };

  return (
    <div>
    {hasAccount ? (
    <div>
      <header>
        <h2>Your MateoMonedas Wallet</h2>
        <br />
        <br />
      </header>
      <img src={user.picture} alt="User" className="account-image" />
      <table style={{margin:'20px'}}>
      <tbody>
          <tr>
            <td>email</td>
            <td className='a'>{user.email}</td>
          </tr>
          <tr>
            <td>public-key </td>
            <td className='b'> 
              <pre>{public_key}</pre>
            </td>
            <td>
              <button onClick={handleCopyPublicKey} className="copy-button">
                copy
              </button>
            </td>
          </tr>
          <tr>
            <td>balance </td>
            <td className='a'>{`${balance} mm`}</td>
          </tr>
        </tbody>
      </table>  
      <Transaction user={user} />
      <Miner user = {user}/>
    </div>
    ) : (
      <HandleAccount user={user} />
    )}
    </div>
  );
}

export default Account;