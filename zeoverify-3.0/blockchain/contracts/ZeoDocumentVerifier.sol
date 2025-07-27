// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ZeoDocumentVerifier {
    address public owner;

    mapping(bytes32 => bool) public verifiedDocs;

    event DocumentVerified(bytes32 indexed docHash, address indexed verifier);

    constructor() {
        owner = msg.sender;
    }

    function verifyDocument(bytes32 docHash) public {
        require(!verifiedDocs[docHash], "Already verified");
        verifiedDocs[docHash] = true;
        emit DocumentVerified(docHash, msg.sender);
    }

    function isVerified(bytes32 docHash) public view returns (bool) {
        return verifiedDocs[docHash];
    }
}
