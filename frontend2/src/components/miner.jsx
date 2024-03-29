import axiosInstance from "./api";
import React from "react";


function Miner({ user }) {
  const mine = () => {
    console.log("Mining...");
    axiosInstance
      .get(`/mine/${user.sub}`)
      .then(response => response.data)
      .then(text => 
        {console.log(text);
        alert(`${text}, reload the page to see if someone has given you mateomoneadas`);
      })
      .catch(error => console.error(error)); 
  };

  return (
    <>
    <div style={{ display: 'flex', justifyContent: 'center', margin: '20px' }}>
      <button onClick={mine}>Mine block</button>
    </div>
    <div>
      <h3>If you want to help us complete all pending transactions, mine a block and obtain 1 mateomoneda as a reward!</h3>
    </div>
    </>
  );
}

export default Miner;