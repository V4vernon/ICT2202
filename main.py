from brownie import *
p = project.load("brownie", name="BrownieProject")
p.load_config()
from brownie.project.BrownieProject import *
from brownie.network import priority_fee, max_fee, web3
#from web3 import Web3, IPCProvider, HTTPProvider
#from web3.logs import STRICT, IGNORE, DISCARD, WARN
#from web3.middleware import geth_poa_middleware
import json
import asyncio
import time

def print_transaction(tx, w3):
  print("=============================================================")
  print("nonce: {0}".format(tx["nonce"]))
  print("blockHash: {0}".format(tx["blockHash"].hex()))
  print("blockNumber: {0}".format(tx["blockNumber"]))
  print("transactionIndex: {0}".format(tx["transactionIndex"]))
  print("from: {0}".format(tx["from"]))
  print("to: {0}".format(tx["to"]))
  print("value: {0}".format(Web3.fromWei(tx["value"], "ether")))
  print("gasPrice: {0}".format(tx["gasPrice"]))
  print("gas: {0}".format(tx["gas"]))
  decode_contract_data(tx, w3)
  print("=============================================================")
  print()

def print_block(block):
  print("###########################################################################")
  print("hash: {0}".format(block["hash"].hex()))
  print("parentHash: {0}".format(block["parentHash"].hex()))
  print("nonce: {0}".format(block["nonce"].hex()))
  print("sha3Uncles: {0}".format(block["sha3Uncles"].hex()))
  print("logsBloom: {0}".format(block["logsBloom"].hex()))
  print("transactionsRoot: {0}".format(block["transactionsRoot"].hex()))
  print("stateRoot: {0}".format(block["stateRoot"].hex()))
  print("difficulty: {0}".format(block["difficulty"]))
  print("totalDifficulty: {0}".format(block["totalDifficulty"]))
  print("size: {0}".format(block["size"]))
  print("gasLimit: {0}".format(block["gasLimit"]))
  print("gasUsed: {0}".format(block["gasUsed"]))
  print("timestamp: {0}".format(block["timestamp"]))
  txs = block["transactions"]
  for tx in txs:
    print(tx.hex())
  uncles = block["uncles"]
  for u in uncles:
    print(u.hex())
  print("proofOfAuthorityData {0}".format(block["proofOfAuthorityData"].hex()))
  print("###########################################################################")
  print()
  
def decode_contract_data(tx, w3):
  if (tx["to"] == "0xd5a26D595026cDDB18D326bD33c042240475595c"):
    f = open("/home/works/Desktop/abi.json")
    abi = json.load(f)
    f.close()
    ByteABlock = w3.eth.contract(address="0xd5a26D595026cDDB18D326bD33c042240475595c", abi=abi)
    func_obj, func_params = ByteABlock.decode_function_input(tx["input"])
    print("input: ")
    print(func_obj)
    print(func_params)
    print()
  else:
    print("input: {0}".format(tx["input"]))
    
def main():
  network.connect("Block-testnet")
  #ByteABlock.deploy({'from':accounts[0], 'gas_price': 0})

  # w3 = Web3(HTTPProvider("http://127.0.0.1:8501"))

  # w3.middleware_onion.inject(geth_poa_middleware, layer=0)

  # print(ByteABlock[0].abi)

  print(web3.clientVersion)
  latest = web3.eth.block_number
  latest_tx = web3.eth.get_transaction_by_block(latest, 0)
  tx_hash = latest_tx["hash"]

  rf = open("abi.json", "r")
  abi = json.load(rf)
  rf.close()
  contract = web3.eth.contract(address="0x44fe55eb077ac62A467a1A8522415C255bb0C6Cd", abi=abi)
  add_item_filter = contract.events.evidenceAdded.createFilter(fromBlock=0, argument_filters={"_caseId":1})
  change_filter = contract.events.statusChanged.createFilter(fromBlock=0, argument_filters={"_caseId": 1, "_evidId": 1})

  # Get information from the transactionReceipt Object
  # tx = chain.get_transaction(tx_hash)
  # print(tx.contract_name)
  # print(tx.fn_name)
  # print(ByteABlock[0].decode_input(tx.input))
  # print(tx.events)
  # print(tx.logs)
  # print(tx.status)

  # Export application binary interface of contract
  # with open("abi.json", "w") as f:
  #   json.dump(ByteABlock[0].abi, f, indent=4)
  # tx = chain.get_transaction("0x6ec70e97e93f6b81ca9f76f9747d7dfb63dd2cf280dc029b308c190e25bc46e1")
  # print(tx)
  # print(tx.events)
  ByteABlock[0].addEvidenceItem(1,2,1,"SIT","4523agvc","Storage","4673","WD SN550","In Transit","","Device is operational", {'from': accounts[0], 'gas_price':1})
  evidence = ByteABlock[0].centralStore(1,1)
  print(evidence)
  ByteABlock[0].modifyEvidenceStatus(1,1,2,"For Storage","Check-In for Storage",{'from': accounts[0], 'gas_price':1})
  ByteABlock[0].modifyEvidenceStatus(1,1,1,"For Analysis","Check-In for Analysis",{'from': accounts[0], 'gas_price':1})
  ByteABlock[0].modifyEvidenceStatus(1,2,1,"For Analysis","Check-In for Analysis",{'from': accounts[0], 'gas_price':1})
  # time.sleep(5)
  evidence1 = ByteABlock[0].centralStore(1,1)
  evidence2 = ByteABlock[0].centralStore(1,2)
  print(evidence1)
  print(evidence2)

  print(add_item_filter.get_all_entries())
  print(change_filter.get_all_entries())
  # ByteABlock[0].addEvidenceItem(1,6,6,"SIT","3452gwrt","Storage","8911","WD SN550","Good","In Transit","NIL", {'from': accounts[0]})

if __name__ == "__main__":
  main()
