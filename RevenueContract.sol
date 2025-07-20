// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RevenueContract {
    mapping(uint => uint) public videoRevenues;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function recordRevenue(uint videoId, uint amount) public {
        require(msg.sender == owner, "Only owner can record revenue");
        videoRevenues[videoId] += amount;
    }

    function getRevenue(uint videoId) public view returns (uint) {
        return videoRevenues[videoId];
    }
}
