# Home of what powers Byte-A-Block
Hi, welcome to the blockchain home of the Byte-A-Block project. Feel free to look around and make yourself at home.

## Getting Started

### Prerequisites
1) Geth (Go-Ethereum)

    `sudo apt install ethereum`
    
    
2) Python 3.7

    `sudo apt install python3.7`

3) Eth-Brownie (Python Ethereum Smart Contract Framework)

    `pip install eth-brownie`
    
4) Linux VM running Ubuntu 18.04

5) VPN to simulate a private network over the internet (more only for security reasons)

    `sudo apt install wireguard`
    
    As this is not crucial to the workings of the project, as in the ethereum nodes can also connect on public IPs, you can find more information about how to setup a wireguard VPN network below, and while it is for 20.04, it works well on 18.04 too.
    
    https://www.cyberciti.biz/faq/ubuntu-20-04-set-up-wireguard-vpn-server/
    
### Setting Up
Once you have installed the prerequisities, we can move on to the actual node setup. Given the need for security as our chain involves the storage of information with regards to the physical media containing digital evidence, we opted to add nodes manually to the chain and turn off autodiscovery for nodes

We wrote a bash script to simplify the setup process somewhat, especially some of the repetitive steps.

Firstly to start setting up, run this in your terminal, on every single VM that should be added to the network (more clarifications on this later)

`./chain_setup`

This should present you with a few options, that looks like the image below:

![chain_setup_main](https://user-images.githubusercontent.com/20734215/139518739-825bf142-396f-4ca1-ab20-7ff74586d838.PNG)

Secondly, we need to gather the public ethereum wallet addresses of each of the nodes.
We can obtain this by inputting option 1 to setup the ethereum node

![chain_setup_1](https://user-images.githubusercontent.com/20734215/139519087-c7333072-8392-4f29-bc9c-671cf51f6c13.PNG)

This would create two nodes and generate their respective public and private wallet addresses. The public addresses would be written to the nodes_info.txt file, which looks like this:

![chain_setup_addresses](https://user-images.githubusercontent.com/20734215/139519149-bf93a036-5723-42d8-8332-f9ee88cce29a.PNG)

The script would ask you if you want to initialize the nodes, which you can safely just say no to for now

We are only using node1, so ignore the second wallet address. Note this down, as it would be used in the generation of the genesis file.

**Repeat the above steps on every single node that should be added to the network, and collect their public wallet addresses**

Thirdly, once we have all the public wallet addresses of each of the nodes in hand. We can then generate the genesis file.

To do so, run puppeth, which comes with the ethereum (geth) package we installed earlier

`puppeth`

You should then be greeted with a screen that looks like this. Under the network name to administer, specify byteablock

![Puppeth_Network_Name](https://user-images.githubusercontent.com/20734215/139519381-7260f6ae-c8b0-4987-b2e8-5edec2514329.PNG)

Next, you would see a screen offering options you can perform. Select Option 2 (Configure New Genesis)

![Configure_New_Genesis](https://user-images.githubusercontent.com/20734215/139519475-1b9e1eb4-dbc8-4c36-a190-7d7d9e2ed990.PNG)

Afterwhich, select Option 1 (Create new genesis from scratch)

![Create_New_Genesis](https://user-images.githubusercontent.com/20734215/139519535-9ff1c734-5fb7-4bab-ad4c-f322bcde8698.PNG)













    
### 

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


