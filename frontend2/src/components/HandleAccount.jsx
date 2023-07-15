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
        <h3 className="account-message">
            You do not have an account, create an account to continue
        </h3>
        <button onClick={handleClick} className="account-button">
            Create Account
        </button>
        </header>
    </div>
  );
};

export default HandleAccount;
