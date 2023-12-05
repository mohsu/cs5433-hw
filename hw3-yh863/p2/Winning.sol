// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EtheremonLite {
    function initMonster(string memory _monsterName) public {}

    function getName(
        address _monsterAddress
    ) public view returns (string memory) {}

    function getNumWins(address _monsterAddress) public view returns (uint) {}

    function getNumLosses(address _monsterAddress) public view returns (uint) {}

    function battle() public returns (bool) {}
}

contract WinBattle {
    EtheremonLite etheremonLite;

    constructor() {
        etheremonLite = EtheremonLite(
            address(0x04EAB7C83B2F45bDbE9DF44E337740bbdFe5efDE)
        );
        etheremonLite.initMonster("yh863");
    }

    function fight() public {
        uint battleRatio = 3;
        uint dice = uint(blockhash(block.number - 1));
        dice = dice / 2;

        if (dice % battleRatio == 0) {
            etheremonLite.battle();
        }
    }
}
