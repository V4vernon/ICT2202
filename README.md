# Home of what powers Byte-A-Block
Hi, welcome to the blockchain home of the Byte-A-Block project. Feel free to look around and make yourself at home.

## Setup
Make sure you have eth-brownie and geth installed

## Brownie Stuff
### Initialize new brownie project
`brownie init`
### Add a network
`brownie networks add live VPN host=http://10.7.0.6:8501 chainid=10117 name="VPN Network"`

## Geth Debug
```
geth attach geth.ipc -exec admin.nodeInfo.enode
geth attach geth.ipc -exec admin.peers
geth attach geth.ipc -exec admin.addPeer("0x...")
```


