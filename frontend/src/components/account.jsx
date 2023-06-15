import React, { useState, useEffect } from 'react';
import '../style/account.css';
import Miner from './miner';
import Transaction from './transaction';
import HandleAccount from './HandleAccount';

function Account({ user }) {
  var funds = 0;
  const [public_key, setPublicKey] = useState();
  const [hasAccount, setAccount] = useState(false);

  useEffect(() => {
    const fetchPublicKey = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5010/public_key/${user.sub}`);
        if (response.status === 404){
          setPublicKey("No public key found");
        }
        else{
          const publicKey = await response.text();
          setPublicKey(publicKey);
        }
      } catch (error) {
        console.error('Error fetching public key:', error);
      }
    };
    
    fetchPublicKey();
  }, [user.sub]);

  const handleCopyPublicKey = () => {
    navigator.clipboard.writeText(public_key);
  };

  return (
    <div>
    {hasAccount ? (
    <div>
      <header>
        <h2>MateoMonedas Account Profile</h2>
        <br />
        <br />
      </header>
      <img src={user.picture} alt="User" className="account-image" />
      <table style={{margin:'20px'}}>
      <tbody>
          <tr>
            <td>Email</td>
            <td className='a'>{user.email}</td>
          </tr>
          <tr>
            <td>Public key </td>
            <td className='b'> 
              {public_key}
            </td>
            <td>
              <button onClick={handleCopyPublicKey} className="copy-button">
                Copy key
              </button>
            </td>
          </tr>
          <tr>
            <td>Balance </td>
            <td className='a'>{funds}</td>
          </tr>
        </tbody>
      </table>  
      <Transaction user={user} />
      <Miner />
    </div>
    ) : (
      <HandleAccount user={user} setAccount={setAccount} />
    )}
    </div>
  );
}

export default Account;
