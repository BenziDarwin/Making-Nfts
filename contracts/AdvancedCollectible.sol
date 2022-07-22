//SPDX-License-Identifer: MIT
pragma solidity >=0.8.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public randomNumber;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event RequestedCollectible(bytes32 indexed requestId, address sender);
    event CreateBreed(uint256 indexed tokenId, Breed breed);
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) ERC721("Dogie", "DOG") VRFConsumerBase(_vrfCoordinator, _link) {
        tokenCounter = 0;
        keyHash = _keyHash;
        randomNumber = 0;
        fee = _fee;
    }

    function createCollectible() public {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = _msgSender();
        emit RequestedCollectible(requestId, _msgSender());
    }

    function fulfillRandomness(bytes32 requestId, uint256 _randomNumber)
        internal
        override
    {
        randomNumber = _randomNumber;
        uint256 newTokenId = tokenCounter;
        Breed breed = Breed(randomNumber % 3);
        tokenIdToBreed[newTokenId] = breed;
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        emit CreateBreed(newTokenId, breed);
        tokenCounter += 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // Three token URIs are required for pug, shiba_inu, and st_benard.
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: Is not owner or approved!"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
