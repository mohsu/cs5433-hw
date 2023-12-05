from solcx import compile_source
from web3 import Web3, Account

w3 = Web3(Web3.HTTPProvider(
    'https://sepolia.infura.io/v3/23a668257ecb4ece82ff765e85972ef7'))
assert w3.is_connected(), "Web3 is not connected to the Ethereum network!"
private_key = "0xd0d87fa4b6f9758dd2151efa78671331f206e3327e44eb69837b547c8e62c320"
account = Account.from_key(private_key)
print(account.address)
w3.eth.default_account = account.address

with open("./05_bad_ico.sol") as f:
    contract_source_code = f.read()

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:TestToken']

###### DEPLOY CONTRACT ########
# deploy contract on the blockchain by Remix

contract_address = "0x2Ab121B8f7A4aD620321adF35Cc7Dd541B829ed6"
my_contract = w3.eth.contract(
    address=contract_address,
    abi=contract_interface['abi'])


def call_function(function, *arg, gas_limit=200000, value=0):
    nonce = w3.eth.get_transaction_count(account.address)
    txn = function(*arg).build_transaction({
        'from': account.address,
        'gas': gas_limit,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'value': value
    })
    signed_txn = Account.sign_transaction(txn, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(txn_receipt)


call_function(my_contract.functions.deposit, value=3133700000000000)
call_function(my_contract.functions.depositwithbonus, value=20000)
print("Current contract balance: ", w3.eth.get_balance(contract_address))
print("Current total supply: ", my_contract.functions.totalSupply().call())
