import axiosInstance from "../axiosApi";

const fetchBalance = async () => {
    try {
      const response = await axiosInstance.get(`/balance/${user.sub}`);
      const balance_resp = await response.data;
      setBalance(balance_resp);
    } catch (error) {
      console.error('Error fetching balance:', error);
      setBalance("No balance found");
      setAccount(false);
    }
  };