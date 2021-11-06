// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract ByteABlock {
    
    struct evidenceItem {
        uint handlerId;
        string location;
        string imageHash;
        string evidType;
        string serialNo;
        string model;
        string currStatus;
        string purpose;
        string notes;
    }
    
    mapping(uint => mapping(uint => evidenceItem)) public centralStore;
    
    event evidenceAdded(uint indexed _caseId, uint indexed _evidId, uint indexed _handlerId, string _currStatus, string _serialNo, uint256 date);
    event statusChanged(uint indexed _caseId, uint indexed _evidId, uint indexed _handlerId, string _currStatus, string _imageHash, string _purpose, uint256 date);
    
    function addEvidenceItem(
        uint _caseId, uint _evidId, uint _handlerId,
        string memory _location, string memory _imageHash, string memory _evidType, 
        string memory _serialNo, string memory _model, 
        string memory _currStatus, string memory _purpose, string memory _notes
        ) public {
            centralStore[_caseId][_evidId] = evidenceItem(_handlerId, _location, _imageHash, _evidType, _serialNo, _model, _currStatus, _purpose, _notes);
            emit evidenceAdded(_caseId, _evidId, _handlerId, _currStatus, _serialNo, block.timestamp);
        }
        
    function modifyEvidenceStatus(uint _caseId, uint _evidId, uint _handlerId, string memory _newStatus, string memory _imageHash, string memory _purpose) public{
        centralStore[_caseId][_evidId].currStatus = _newStatus;
        centralStore[_caseId][_evidId].handlerId = _handlerId;
        centralStore[_caseId][_evidId].imageHash = _imageHash;
        centralStore[_caseId][_evidId].purpose = _purpose;
        emit statusChanged(_caseId, _evidId, _handlerId, _newStatus, _imageHash, _purpose, block.timestamp);
    }
    
}
