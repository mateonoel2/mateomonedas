function Miner() {

    const mine = () => {
        console.log("Mining...");
    }
    return(
        <div style={{ display: 'flex', justifyContent: 'center', margin: '20px' }}>
        <button onClick={mine} >
          Mine block
        </button>
      </div>
    )
}

export default Miner;