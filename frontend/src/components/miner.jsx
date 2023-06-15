import '../App.css';

function Miner() {

    const mine = () => {
        console.log("Mining...");
    }
    return(
        <div>
            <header>
                <button onClick={(mine)}>Mine block</button>
            </header>
        </div>
    )
}

export default Miner;