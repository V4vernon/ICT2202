from web3 import Web3, IPCProvider, HTTPProvider
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from web3.middleware import geth_poa_middleware
import json
import asyncio

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
    
def handle_event(event):
    print(event.hex())

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

def main():
  # w3 = Web3(IPCProvider("~/ByteABlock/node1/geth.ipc"))
  w3 = Web3(HTTPProvider("http://10.7.0.6:8501"))

  w3.middleware_onion.inject(geth_poa_middleware, layer=0)

  print(w3.clientVersion)

  # w3 = Web3(Web3.HTTPProvider('http://localhost:8501'))

  print(w3.eth.get_block('latest'))
  print()
  latest_tx = w3.eth.get_transaction_by_block('latest', 0)
  tx_hash = latest_tx["hash"]
  receipt = w3.eth.get_transaction_receipt(tx_hash)
  f = open("/home/works/Desktop/abi.json")
  abi = json.load(f)
  f.close()
  ByteABlock = w3.eth.contract(address="0xd5a26D595026cDDB18D326bD33c042240475595c", abi=abi)
  processed_log = ByteABlock.events.evidenceAdded().processReceipt(receipt)
  print(processed_log)
  
  print(w3.eth.accounts)
  print()
  print(w3.fromWei(w3.eth.get_balance('0xf1f849FF49b54d449FF2681E61a4A5d2fAF231a8'), "ether"))

  # sender = "0xf1f849FF49b54d449FF2681E61a4A5d2fAF231a8"
  # receiver = "0x816266387273Eba271b6A20EF228b17504e0fbc8"

  # amount = w3.toWei(1, 'ether')

  # w3.eth.send_transaction({
  #   'to': receiver,
  #   'from': sender,
  #   'value': amount
  # })

  # fil = w3.eth.filter({'address': '0xf1f849FF49b54d449FF2681E61a4A5d2fAF231a8'})
  # w3.eth.uninstall_filter(fil.filter_id)

  latest = w3.eth.block_number
  for i in range(0,latest):
    block = w3.eth.get_block(latest - i)
    print_block(block)
    tx = w3.eth.get_transaction_by_block(latest - i, 0)
    print_transaction(tx, w3)
    print()
    
  block_filter = w3.eth.filter('latest')
  loop = asyncio.get_event_loop()
  try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, 2)))
  finally:
        loop.close()

if __name__ == "__main__":
  main()

