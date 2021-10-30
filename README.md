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

#### Getting Wallet Public Addresses
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

Lastly, the script would ask you if you want to initialize the nodes, which you can safely just say no to for now

We are only using node1, so ignore the second wallet address. Note this down, as it would be used in the generation of the genesis file.

*NOTE: Repeat the above steps on every single node that should be added to the network, and collect their public wallet addresses*

#### Creating the project genesis file
Once we have all the public wallet addresses of each of the nodes in hand, we can generate the genesis file.

To do so, run puppeth, which comes with the ethereum (geth) package we installed earlier

`puppeth`

Firstly, you should then be greeted with a screen that looks like this. Under the network name to administer, specify byteablock

![Puppeth_Network_Name](https://user-images.githubusercontent.com/20734215/139519381-7260f6ae-c8b0-4987-b2e8-5edec2514329.PNG)

Secondly, you would see a screen offering options you can perform. Select Option 2 (Configure New Genesis)

![Configure_New_Genesis](https://user-images.githubusercontent.com/20734215/139519475-1b9e1eb4-dbc8-4c36-a190-7d7d9e2ed990.PNG)

Thirdly, select Option 1 (Create new genesis from scratch)

![Create_New_Genesis](https://user-images.githubusercontent.com/20734215/139519535-9ff1c734-5fb7-4bab-ad4c-f322bcde8698.PNG)

Following Which, select Option 2 (Clique - proof-of-authority)

![Consensus_Engine](https://user-images.githubusercontent.com/20734215/139520749-008a3d11-4e4d-402d-8e29-a7edd4b5abfd.PNG)

Fourthly, for how many seconds should blocks take, enter 0 (meaning that a new block would only be created when there is a new transaction)

![Block_Seconds](https://user-images.githubusercontent.com/20734215/139520881-caa023c0-c3fb-4cbf-bedf-ed02fc8726e6.PNG)

Fifthly, for which accounts are allowed to seal, specify the public wallet addresses of all the nodes, an example for one node is shown below

![Sealer_Accounts](https://user-images.githubusercontent.com/20734215/139520989-fc7476c5-9700-4f03-8185-f9217f01f235.PNG)

Afterwhich, do the same thing as above for which accounts should be prefunded

![PreFund](https://user-images.githubusercontent.com/20734215/139521037-58264e29-b5f1-43f2-b037-897aa05fbc36.PNG)

Following which, for whether precompile addresses should be funded, enter yes, though these accounts would be deleted later

Then, for chain/network ID specify one of your choosing, or enter to accept a randomly generated ID

![Chain_ID](https://user-images.githubusercontent.com/20734215/139521114-887ad0b5-9eb3-4e70-a347-ed8093e81e2f.PNG)

Finally, you're done inputting the relevant details for the genesis file. Yay. You should be brought back to this familiar looking screen

![genesis_process_complete](https://user-images.githubusercontent.com/20734215/139521158-ede895d9-0ab2-4665-9700-5242672b90d7.PNG)

Enter 2 to manage your genesis block

Enter 2 for export genesis configuration, followed by enter when asked whether you want to write the files to current directory

![Export_Genesis_1](https://user-images.githubusercontent.com/20734215/139521229-d5768f7a-d9ed-4280-b17e-3de192b70e25.PNG)

![export_genesis_2](https://user-images.githubusercontent.com/20734215/139521286-19d2be21-95b7-4ed2-9e37-259b568fe418.PNG)

Before we sum up, open your genesis file and remove all the precompiled addresses under alloc, or put it simply those public addresses that you did not add manually earlier. Then change the gas limit to 0xe4e1c0 (15000000). Your completed genesis file should look like the byteablock.json present in this repository.

This sums up how to create the genesis file, which only needs to be done once. Next, we need to initialize the nodes with the genesis file we created

#### Initializing the Genesis Block on nodes

To initialize the genesis block for the node, let's go back and use the handy chain_setup script. Similarly select option 1, but this time for the question of whether you want to initialize genesis block, enter yes.

![init_genesis](https://user-images.githubusercontent.com/20734215/139521593-cc6e0953-0a6f-4f9c-b9d6-88f7769925ad.PNG)

*NOTE: This has to be performed on every single node to be added to the network*

#### Running the nodes

1) For new setups

    The chain_setup script can also be used to run the nodes. As it does not know about the details of the nodes initially, follow its steps to add a node definition

    ![Run_Nodes_1](https://user-images.githubusercontent.com/20734215/139521914-b26556fd-ba63-46a3-8727-bf3788b2d7c6.PNG)

    After the relevant details are given, the script will attempt to start a geth node running in the background.
    
    In order for the nodes to find one another, as mentioned earlier we need to add them manually. To do this we need to get the enode id of every node, which kinds of provides a way for other nodes to connect to them, and add them into a static-node.json file to be placed in the node1/geth folder.
    
    This can be done using chain_setup, through selecting option 4 (List your enode id)
    
    ![List_Enode_ID](https://user-images.githubusercontent.com/20734215/139522191-47a7a63e-a00d-488c-b2ac-735a3fd83ee2.PNG)
    
    A sample static-nodes.json file looks like this:
    
    ```
    [
      "enode://xxxxx:port1",
      "enode://yyyyy:port2"
    ]
    ```
    
    After creating and placing the static-nodes.json file in the node1/geth folder, restart your node using step 2 below, for convenience reasons
    
    Then verify that you are connected to the rest of the hosts by running chain_setup again, and entering option 3 (List nodes you are connected to)
    
    ![List_Connected_Nodes](https://user-images.githubusercontent.com/20734215/139522293-0c7c3f76-ef20-4899-bd8c-8981c8be9029.PNG)

2) For existing setups

    If you already have a node definition, and want to run your node, you can follow the steps in the image below
    
    ![Run_Existing_Node](https://user-images.githubusercontent.com/20734215/139522075-2d9b8ff3-0136-4dd3-ba41-44d81035503d.PNG)

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


