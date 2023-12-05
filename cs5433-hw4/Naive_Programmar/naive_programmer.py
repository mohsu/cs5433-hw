from solcx import compile_source
from web3 import Web3, Account
import time

w3 = Web3(Web3.HTTPProvider(
    'https://sepolia.infura.io/v3/23a668257ecb4ece82ff765e85972ef7'))
assert w3.is_connected(), "Web3 is not connected to the Ethereum network!"
private_key = "0xd0d87fa4b6f9758dd2151efa78671331f206e3327e44eb69837b547c8e62c320"
account = Account.from_key(private_key)
print(account.address)
w3.eth.default_account = account.address

with open("./01_naive_programmer.sol") as f:
    contract_source_code = f.read()

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:SourceTrixAreForl337']


###### DEPLOY CONTRACT ######
# MyContract = w3.eth.contract(
#     abi=contract_interface['abi'],
#     bytecode=contract_interface['bin']
# )
# deploy contract on the blockchain
# nonce = w3.eth.get_transaction_count(account.address)
# gas_price = w3.eth.gas_price
# transaction = {
#     'from': account.address,
#     'nonce': nonce,
#     'gasPrice': gas_price,
#     'gas': 3000000,
#     'data': MyContract.constructor().data_in_transaction,
# }
# signed_tx = Account.sign_transaction(transaction, private_key)
# tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(tx_receipt.contractAddress)


###### INTERACT WITH CONTRACT #####
# create contract instance
contract_address = "0xCaCDC1D120db03F496CE7f59dc96b6A245239a3e"
my_contract = w3.eth.contract(
    address=contract_address,
    abi=contract_interface['abi'])
print("ok")

# initiate
nonce = w3.eth.get_transaction_count(account.address)
txn = my_contract.functions.SourceTrixAreFor1337(25, 'Alice', 'Bob').build_transaction({
    'from': account.address,
    'gas': 200000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
})
signed_txn = Account.sign_transaction(txn, private_key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

# # vote for Alice
# _voteCommit = w3.keccak(text="1Alice")
# nonce = w3.eth.get_transaction_count(account.address)
# txn = my_contract.functions.commitVote(_voteCommit).build_transaction({
#     'from': account.address,
#     'gas': 200000,
#     'gasPrice': w3.eth.gas_price,
#     'nonce': nonce,
# })
# signed_txn = Account.sign_transaction(txn, private_key)
# txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

# reveal the vote
# nonce = w3.eth.get_transaction_count(account.address)
# txn = my_contract.functions.revealVote("1Alice", _voteCommit).build_transaction({
#     'from': account.address,
#     'gas': 200000,
#     'gasPrice': w3.eth.gas_price,
#     'nonce': nonce,
# })
# signed_txn = Account.sign_transaction(txn, private_key)
# txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

# constantly swap choice 1 and 2 if Alice is the winner
choice1, choice2 = "Alice", "Bob"
while my_contract.functions.currentWinner().call() != "Bob":
    nonce = w3.eth.get_transaction_count(account.address)
    txn = my_contract.functions.SourceTrixAreFor1337(0, choice2, choice1).build_transaction({
        'from': account.address,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    signed_txn = Account.sign_transaction(txn, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    choice1, choice2 = choice2, choice1

    time.sleep(20)
