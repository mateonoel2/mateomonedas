from flask import Flask, jsonify, request
import requests
from block import Block, Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/blocks', methods=['GET', 'POST'])
def blocks_route():
    if request.method == 'GET':
        # Logic to return the blockchain as JSON
        blockchain_json = jsonify(blockchain.to_json())
        return blockchain_json, 200
    elif request.method == 'POST':
        # Logic to receive and validate a new block
        data = request.get_json()

        # Extract block data from the request
        previous_hash = data.get('previous_hash')
        timestamp = data.get('timestamp')
        transactions = data.get('transactions')
        nonce = data.get('nonce')

        # Create a new block instance
        new_block = Block(previous_hash, timestamp, transactions, nonce)

        new_block.mine_block(blockchain.difficulty)

        # Validate the new block
        if new_block.is_valid():
            # Add the new block to the blockchain
            blockchain.add_block(new_block)
            response = {'message': 'New block added successfully'}
            return jsonify(response), 201
        else:
            response = {'message': 'Invalid block. Rejected.'}
            return jsonify(response), 400


@app.route('/consensus', methods=['GET'])
def consensus():
    # Logic to handle consensus among nodes
    longest_chain = None
    current_length = len(blockchain)

    other_nodes = ['localhost:5010', 'localhost:5011']
    
    # Iterate through other nodes in the network
    for node in other_nodes:
        # Make a GET request to the '/blocks' endpoint of each node
        response = requests.get(f'http://{node}/blocks')
        if response.status_code == 200:
            # Extract the blockchain from the response
            node_chain = response.json()

            # Get the length of the node's blockchain
            node_length = len(node_chain)

            # Check if the node's blockchain is longer and valid
            if node_length > current_length and blockchain.is_valid_chain(node_chain):
                current_length = node_length
                longest_chain = node_chain

    if longest_chain:
        # Replace the current blockchain with the longest valid chain
        blockchain.replace_chain(longest_chain)
        response = {'message': 'Blockchain replaced with the longest valid chain'}
    else:
        response = {'message': 'Current blockchain is the longest valid chain'}

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012)
