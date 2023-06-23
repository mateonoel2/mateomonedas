import axiosInstance from "./api";
import React from "react";

const HandleAccount = ({ user }) => {  
  const handleClick = async () => {
    try {
      const response = await axiosInstance.post(`/create_account/${user.sub}`);
      const message = await response.data;
      if (message === "Account created successfully") {
        window.location.reload();
      }
    } catch (error) {
      console.error('Error generating public key', error);
    }
  };

  return (
    <div style={{ margin: '20px' }}>
        <header>
        <button onClick={handleClick} className="account-button">
            Generate public key
        </button>
        </header>
    </div>
  );
};

export default HandleAccount;
