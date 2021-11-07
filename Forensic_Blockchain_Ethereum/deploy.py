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
# Deploys a contract and writes its abi to abi.json
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

deploy_and_get_abi()
