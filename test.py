from block import Blockchain

blockchain = Blockchain()

user1 = blockchain.add_user()
user2 = blockchain.add_user()




blockchain.add_transaction(user1, user2, 10)
blockchain.add_transaction(user2, user1, 5)

blockchain.mine_pending_transactions(user1)
blockchain.mine_pending_transactions(user1)

for block in blockchain.chain:
    print(block)

json_representation = blockchain.to_json()
print(json_representation)

is_valid = blockchain.is_valid_chain(blockchain.chain)
print(f"Is blockchain valid? {is_valid}")

p1 = blockchain.get_user_balance(user1)
p2 = blockchain.get_user_balance(user2)

print(f"User 1 balance: {p1}")
print(f"User 2 balance: {p2}")

chain_length = len(blockchain)
print(f"Chain length: {chain_length}")