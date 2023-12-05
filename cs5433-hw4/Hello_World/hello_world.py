from web3 import Web3, EthereumTesterProvider, Account, utils
from eth_tester import EthereumTester
from solcx import compile_source
import json

w3 = Web3(Web3.HTTPProvider(
    'https://sepolia.infura.io/v3/23a668257ecb4ece82ff765e85972ef7'))
# print(w3.is_connected())
assert w3.is_connected(), "Web3 is not connected to the Ethereum network!"
# w3.eth.default_account = "0x3C4d46281Ace9ddd5fAB8438B6dfB92C553860E0"
private_key = "0xd0d87fa4b6f9758dd2151efa78671331f206e3327e44eb69837b547c8e62c320"
account = Account.from_key(private_key)
print(account.address)
w3.eth.account = account

contract_address = '0xd509b7bded5581ce089b66b075191bb65879d8c1'
compiled_sol = compile_source("""pragma solidity^0.5.0;

contract HelloWorldContract {
    bytes32 public ownerflag;
    bytes32 public userflag;

    event HelloWorld(string, bytes32);

    constructor(bytes32 _ownerflag) public {
        ownerflag = _ownerflag;
    }

    function helloworld(string memory _yourstring, bytes32 _yourflag) public {
        emit HelloWorld(_yourstring, _yourflag);
        userflag = _yourflag;
    }
}
""", output_values=["abi", "bin"])
contract_id, contract_interface = compiled_sol.popitem()
bytecode = contract_interface['bin']
abi = contract_interface["abi"]

# Create a contract instance
contract = w3.eth.contract(
    address=Web3.to_checksum_address(contract_address), abi=abi)

yourstring = "yh863"
yourflag = "0x3030303030303030303030303030303030303030303030303030307968383633"

nonce = w3.eth.get_transaction_count(account.address)
txn = contract.functions.helloworld(yourstring, yourflag).build_transaction({
    'from': account.address,
    'gas': 200000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce
})

signed_txn = Account.sign_transaction(txn, private_key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(txn_receipt)
