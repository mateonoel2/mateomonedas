import hashlib
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def timestamp_str():
    timestamp = datetime.timestamp(datetime.now())
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


class Transaction:
    def __init__(self, sender, recipient, amount, private_key=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.private_key = private_key
        self.signature = None
    
    def __str__(self):
        sender_key_str = self.sender.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

        recipient_key_str = self.recipient.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
    
        return f"Transaction(Sender: {sender_key_str}, Recipient: {recipient_key_str}, Amount: {self.amount})"

    
    def sign(self):
        if self.private_key is None:
            raise ValueError("Private key is not set.")
        
        transaction_data = str(self.sender.public_bytes) + str(self.recipient.public_bytes) + str(self.amount)
        hash_obj = hashlib.sha256(transaction_data.encode()).digest()
        signature = self.private_key.sign(
            hash_obj,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.signature = signature
    
    def verify_signature(self):
        if self.signature is None:
            raise ValueError("Signature is not set.")
        
        transaction_data = str(self.sender.public_bytes) + str(self.recipient.public_bytes) + str(self.amount)
        hash_obj = hashlib.sha256(transaction_data.encode()).digest()
        try:
            self.sender.verify(
                self.signature,
                hash_obj,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def to_dict(self):
        # Convert the transaction to a dictionary representation
        return {
            "sender": self.sender.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode(),
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature.hex() if self.signature else None
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
        transactions_str = "\n".join(str(transaction) for transaction in self.transactions)
        return f"Block Hash: {self.hash}\nPrevious Hash: {self.previous_hash}\nTimestamp: {self.timestamp}\nTransactions: {transactions_str}\nNonce: {self.nonce}"

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Set the mining difficulty
        self.pending_transactions = []
        self.users = {} 

    genesis_private_key = rsa.generate_private_key(65537, 512)
    genesis_public_key = genesis_private_key.public_key()
    
    def __len__(self):
        # Return the length of the chain
        return len(self.chain)

    def create_genesis_block(self):
        transaction = Transaction(self.genesis_public_key, self.genesis_public_key, 0)
        return Block("0", timestamp_str(), [transaction], 0)
    
    def generate_key_pair(self):
        # Generate a new RSA key pair for a user
        private_key = rsa.generate_private_key(65537, 512)
        public_key = private_key.public_key()
        
        return public_key, private_key
    
    def add_user(self):
        # Add a new user to the blockchain with a generated key pair
        public_key, private_key = self.generate_key_pair()
        self.users[public_key] = private_key
        return public_key

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

    def add_transaction(self, sender, recipient, amount):
        # Create a new transaction and sign it
        private_key = self.users.get(sender)
        if private_key is None:
            raise ValueError("Invalid sender.")

        transaction = Transaction(sender, recipient, amount, private_key)
        transaction.sign()

        if not transaction.verify_signature():
            raise ValueError("Invalid transaction signature.")

        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_reward):
        # Create a new block with the pending transactions and mine it
        block = Block(self.get_last_block().hash, timestamp_str(), self.pending_transactions, 0)
        block.mine_block(self.difficulty)
        self.chain.append(block)

        # Reset the pending transactions and add the miner reward transaction
        self.pending_transactions = [Transaction(self.genesis_public_key, miner_reward, 1)]
    
    def get_user_balance(self, user):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == user:
                    balance -= transaction.amount
                if transaction.recipient == user:
                    balance += transaction.amount
        return balance

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