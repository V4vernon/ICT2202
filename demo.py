from brownie import *
p = project.load("brownie", name="BrownieProject")
p.load_config()
from brownie.project.BrownieProject import *
from brownie.network import priority_fee, max_fee, web3
from brownie.convert import to_string
import json
import asyncio
import time

# Use this function to get the image hash of a given evidence
# Inputs: transaction hash of event, brownie contract
# Outputs: Image Hash of the evidence that was input
def get_image_hash(tx_hash, br_contract):
    tx = chain.get_transaction(tx_hash)
    return br_contract.decode_input(tx.input)[1][4]

# Helper function
# Deploys a contracts and writes its abi to abi.json
def deploy_and_get_abi():
    ByteABlock.deploy({'from':accounts[0], 'gas_price': 0})
    with open("abi.json", "w") as f:
        json.dump(ByteABlock[0].abi, f, indent=4)

# Gets address of the deployed contract, usually the first block
def get_deployed_contract_addr():
    deploy_tx = web3.eth.get_transaction_by_block(1, 0)
    deploy_tx_hash = deploy_tx["hash"]
    tx = chain.get_transaction(deploy_tx_hash)
    return tx.contract_address


# Connect to the blockchain network
# Add a network to brownie through brownie networks add BROWNIE_NETWORK_GROUP BROWNIE_NETWORK_ID host=http://NODE_IP:NODE_PORT chainid=NETWORK_ID name=FRIENDLY_NETWORK_NAME
# i.e. brownie networks add live VPN host=http://10.7.0.6:8501 chainid=10117 name="VPN Network"
network.connect("byteablock")

print(web3.clientVersion)
print()

# Getting information about transactions from block
print("Getting information about latest transaction")
latest = web3.eth.block_number
latest_tx = web3.eth.get_transaction_by_block(latest, 0)
tx_hash = latest_tx["hash"]

# Load the application binary interface (abi), required to get a deployed contract from the chain
rf = open("abi.json", "r")
abi = json.load(rf)
rf.close()

# Get the deployed contract from the chain as a brownie contract object
contract = Contract.from_abi("ByteABlock", "0x000e7cE22b6f63EA7E75408a61649F798538F05E", abi=abi)

# Getting information about transaction from block (continued)
# Get information from the transactionReceipt Object
tx = chain.get_transaction(tx_hash)
print(tx.contract_name)
print(tx.fn_name)
# print(contract.decode_input(tx.input))
print(tx.events)
print(tx.logs)
print(tx.status)
print(tx.timestamp)
print()

# Retrieve items from the chain using centralStore getter
# centralStore(_caseId, _evidenceId)
print("Getting information from blockchain via smart contract getter")
print(contract.centralStore(1,1))
print(contract.centralStore(1,1)[0])
print(contract.centralStore(1,1)[1])
print()

# Add an evidence item to the chain
# addEvidenceItem(
#        uint _caseId, uint _evidId, uint _handlerId,
#        string memory _location, string memory _imageHash, string memory _evidType, 
#        string memory _serialNo, string memory _model, 
#        string memory _currStatus, string memory _purpose, string memory _notes
# )
# emits evidenceAdded(_caseId, _evidId, _handlerId, _currStatus, _serialNo, block.timestamp)
# Remove the .call after the method name to execute the actual transaction
contract.addEvidenceItem.call(1,3,1,"SIT","4523agvc","Storage","4673","WD SN550","In Transit","","Device is operational", {'from': accounts[0], 'gas_price':0})
contract.addEvidenceItem.call(2,4,1,"SIT","4523agvc","Storage","4673","WD SN550","In Transit","","Device is operational", {'from': accounts[0], 'gas_price':0})

# Change the status of an existing evidence item
# modifyEvidenceStatus(uint _caseId, uint _evidId, uint _handlerId, string memory _newStatus, string memory _imageHash, string memory _purpose)
# emit statusChanged(_caseId, _evidId, _handlerId, _newStatus, _imageHash, _purpose, block.timestamp)
# Remove the .call after the method name to execute the actual transaction
contract.modifyEvidenceStatus.call(1,1,2,"For Storage","1492dbcf","Check-In for Storage",{'from': accounts[0], 'gas_price':0})

# Get the deployed contract from the chain as a web3 contract object (required for using filters)
contract_w3 = web3.eth.contract(address="0x000e7cE22b6f63EA7E75408a61649F798538F05E", abi=abi)
# print(contract_w3.centralStore(1,2))
# If you want to use web3 to call contract functions, reference web3.py documentationb

# Create filters for the evidenceAdded and statusChanged events
# evidenceAdded: keeps track of all the evidences added to a case
# statusChanged: keeps track of all the status changes to a particular evidence (ie. Check-In/Out)
# Change fromBlock to 'latest' to get new changes since filter is set up
add_item_filter = contract_w3.events.evidenceAdded.createFilter(fromBlock=1, argument_filters={"_caseId":2})
# add_item_filter = contract_w3.events.evidenceAdded.createFilter(fromBlock=1)
change_filter = contract_w3.events.statusChanged.createFilter(fromBlock=1, argument_filters={"_caseId": 1, "_evidId": 1})

# Get the results that you want after setting up the filters, results will differ based on what filter is it for, and when results are retrieved
# Use get_new_entries() to only get new changes since the block specified in fromBlock
# Use get_all_entries() to get all changes since fromBlock specified in filter
# Reference web3.py documentations on how to call these in a loop, best in an asynchronous manner
added_items = add_item_filter.get_all_entries()
changed_items = change_filter.get_all_entries()

# print("Results from the filter (addEvidence event)")
#print(len(added_items))
# print("Case ID: {}".format(added_items[0]["args"]["_caseId"]))

# COMMENTED OUT AS THERE IS NO EVIDENCE IN THE CHAIN YET
# print("Getting image hash...")
# image_hash = added_items[0]["_imageHash"]
# print(image_hash)
# print(get_image_hash(evt_tx_hash, contract))
# print()
# print(added_items[0]["args"])
# print(added_items[1]["args"])
# print(added_items)
# print(changed_items)
