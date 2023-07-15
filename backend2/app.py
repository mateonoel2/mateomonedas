from functools import wraps
import base64
import json
from flask import Flask, jsonify, request, redirect, session
from flask_cors import CORS
from block import Block, Blockchain
from flask_sqlalchemy import SQLAlchemy
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import html
import os


app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

app.secret_key = os.getenv('API_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    user_sub = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    public_key = db.Column(db.String(1000), nullable=False)
    private_key = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"node('{self.node_address}')"
    
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if 'user' not in session and api_key != f'Bearer {app.secret_key}':
            return 'Unauthorized', 401
        return f(*args, **kwargs)
    return decorated_function

blockchain = Blockchain()

users = {}

@app.route('/api/login/<userID>', methods=['POST'])
def login(userID):
    user = userID
    if user:
        session['user'] = user
        return 'Login successful'
    return 'Invalid username', 401


@app.route('/api/public_key/<userID>', methods=['POST'])
@login_required
def get_public_key(userID):
    try:
        public_key = users[userID]
        key = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        sanitized_key = html.escape(key)
        return sanitized_key
    except:
        return "No user found", 404
    

@app.route('/api/transaction/<userID>', methods=['POST'])
@login_required
def transaction(userID):
        data = request.get_json()
        sender_key = users[userID]
        sender_str = sender_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        print(sender_str)

        recipient = data.get('account')
        recipient = recipient.replace("-----BEGIN PUBLIC KEY----- ", "")
        recipient = recipient.replace(" -----END PUBLIC KEY-----", "")
        recipient = recipient.strip()
        recipient = recipient.replace(" ", "\n")
        recipient = "-----BEGIN PUBLIC KEY-----\n" + recipient +  "\n-----END PUBLIC KEY-----\n"

        print(recipient)

        key_bytes = recipient.encode('utf-8')
        

        recipient_key = serialization.load_pem_public_key(key_bytes, backend=default_backend())
        amount = data.get('amount')

        if (sender_str == recipient):
            return "Cannot send to yourself", 400

        blockchain.add_transaction(sender_key, recipient_key, int(amount))
        return "Transaction added successfully"

@app.route('/api/balance/<userID>', methods=['GET'])
@login_required
def get_balance(userID):
        try:
            key = users[userID]
            balance = blockchain.get_user_balance(key)
            return str(balance)
        except:
            return "No user found", 404
    
@app.route('/api/mine/<userID>', methods=['GET'])
@login_required
def mine(userID):
        blockchain.mine_pending_transactions(users[userID])
        return "Block mined successfully"

@app.route('/api/create_account/<userID>', methods=['POST'])
@login_required
def create_account(userID):
        user_key = blockchain.add_user()
        users[userID] = user_key    
        return "Account created successfully"

@app.route('/api/blocks', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(port=8080)