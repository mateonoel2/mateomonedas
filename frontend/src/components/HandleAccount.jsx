const HandleAccount = ({ user, setAccount }) => {
  const handleClick = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5010/create_account/${user.sub}`,{method: 'POST'});
      const message = await response.text();
      if (message === "Account created successfully") {
        setAccount(true);
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
