import axiosInstance from "./api";
import React from "react";


function Miner({ user }) {
  const mine = () => {
    console.log("Mining...");
    axiosInstance
      .get(`/mine/${user.sub}`)
      .then(response => response.data)
      .then(text => console.log(text))
      .catch(error => console.error(error)); 
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', margin: '20px' }}>
      <button onClick={mine}>Mine block</button>
    </div>
  );
}

export default Miner;