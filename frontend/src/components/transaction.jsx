import React, { useState } from 'react';
import '../style/transaction.css';

function Transaction() {
  const [account, setAccount] = useState('');
  const [amount, setAmount] = useState('');

  const handleAccountChange = (event) => {
    setAccount(event.target.value);
  };

  const handleAmountChange = (event) => {
    setAmount(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Send transaction logic here
    console.log(`Sending transaction to account ${account} with amount ${amount}`);
    // Reset form
    setAccount('');
    setAmount('');
  };

  return (
    <div className="transaction-container">
      <h2>Transaction</h2>
      <form className="transaction-form" onSubmit={handleSubmit}>
        <label>
          Enter Account:
          <input type="text" value={account} onChange={handleAccountChange} />
        </label>
        <br />
        <label>
          Enter Amount:
          <input type="number" value={amount} onChange={handleAmountChange} />
        </label>
        <br />
        <button type="submit">Send Transaction</button>
      </form>
    </div>
  );
}

export default Transaction;
