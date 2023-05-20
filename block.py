import hashlib
import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        # Convert the transaction to a dictionary representation
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }

class Block:
    def __init__(self, previous_hash, timestamp, transactions, nonce):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_header = f"{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}"
        return hashlib.sha256(block_header.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def is_valid(self):
    # Check if the hash of the block is valid
        return self.hash.startswith("0000")

    def __str__(self):
        return f"Block Hash: {self.hash}\nPrevious Hash: {self.previous_hash}\nTimestamp: {self.timestamp}\nTransactions: {self.transactions}\nNonce: {self.nonce}"

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Set the mining difficulty
        self.pending_transactions = []
    
    def __len__(self):
        # Return the length of the chain
        return len(self.chain)

    def create_genesis_block(self):
        # Create the genesis block manually or based on your requirements
        return Block("0", "01/01/2022", "Genesis Block", 0)

    def get_last_block(self):
        # Return the last block in the chain
        return self.chain[-1]

    def add_block(self, new_block):
        # Add a new block to the chain
        new_block.previous_hash = self.get_last_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_valid_chain(self, chain):
        # Check if a given chain is valid
        previous_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block.previous_hash != previous_block.hash:
                return False

            if block.hash != block.calculate_hash():
                return False

            previous_block = block
            current_index += 1

        return True

    def replace_chain(self, new_chain):
        # Replace the current chain with a new chain if it is valid and longer
        if self.is_valid_chain(new_chain) and len(new_chain) > len(self.chain):
            self.chain = new_chain

    def add_transaction(self, transaction):
        # Add a transaction to the pending transactions list
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_reward):
        # Create a new block with the pending transactions and mine it
        block = Block(self.get_last_block().hash, time.time(), self.pending_transactions, 0)
        block.mine_block(self.difficulty)
        self.chain.append(block)

        # Reset the pending transactions and add the miner reward transaction
        self.pending_transactions = [Transaction("Mining Reward", miner_reward, "")]

    def to_json(self):
        # Convert the blockchain to a JSON representation
        json_chain = []
        for block in self.chain:
            json_chain.append({
                "previous_hash": block.previous_hash,
                "timestamp": block.timestamp,
                "transactions": block.transactions,
                "nonce": block.nonce,
                "hash": block.hash
            })
        return json_chain
