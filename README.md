# Home of what powers Byte-A-Block
Hi, welcome to the blockchain home of the Byte-A-Block project. Feel free to look around and make yourself at home.

## Getting Started

### Prerequisites
1) Geth (Go-Ethereum)

    `sudo apt install ethereum`
    
    
2) Python 3.7

    `sudo apt install python3.7 python3.7-dev`

3) Eth-Brownie (Python Ethereum Smart Contract Framework)

    `pip install eth-brownie`
    
4) Linux VM running Ubuntu 18.04

5) VPN to simulate a private network over the internet (more only for security reasons)

    `sudo apt install wireguard`
    
    As this is not crucial to the workings of the project, as in ethereum nodes can also connect on public IPs, you can find more information about how to setup a wireguard VPN network below, and while it is for 20.04, it works well on 18.04 too.
    
    https://www.cyberciti.biz/faq/ubuntu-20-04-set-up-wireguard-vpn-server/
    
### Prerequisites

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

![genesis_export](https://user-images.githubusercontent.com/20734215/139522913-89caede7-3c42-4fad-b996-1df5fd97b996.PNG)


Last but not least, open your genesis file and remove all the precompiled addresses under alloc, or put it simply those public addresses that you did not add manually earlier. Then change the gas limit to 0xe4e1c0 (15000000). Your completed genesis file should look like the byteablock.json present in this repository.

This sums up how to create the genesis file, which only needs to be done once. Next, we need to initialize the nodes with the genesis file we created

#### Initializing the Genesis Block on nodes

To initialize the genesis block for the node, let's go back and use the handy chain_setup script. Similarly select option 1, but this time for the question of whether you want to initialize genesis block, enter yes.

![init_genesis](https://user-images.githubusercontent.com/20734215/139521593-cc6e0953-0a6f-4f9c-b9d6-88f7769925ad.PNG)

Enter the name of the genesis file <PROJECTNAME>.json that you generated earlier when prompted for it. The nodes will then be initialized with the genesis file.

*NOTE: This has to be performed on every single node to be added to the network*

#### Running the Nodes (New Setup)

The chain_setup script can also be used to run the nodes. As it does not know about the details of the nodes initially, follow its steps to add a node definition.

This node definition will be saved in a file, saved_nodes.txt, so subsequent starting of this added node is simpler.

![Run_Nodes_1](https://user-images.githubusercontent.com/20734215/139521914-b26556fd-ba63-46a3-8727-bf3788b2d7c6.PNG)

After the relevant details are given, the script will attempt to start a geth node running in the background.

#### Running the Nodes (Existing Setup)

If you already have a node definition, and want to run your node, you can follow the steps in the image below
    
![Run_Existing_Node](https://user-images.githubusercontent.com/20734215/139522075-2d9b8ff3-0136-4dd3-ba41-44d81035503d.PNG)

This would similarly start a geth node running in the background

### Node Networking

#### Helping nodes find one another

In order for the nodes to find one another, as mentioned earlier we need to add them manually. To do this we need to get the enode id of every node, which kinds of provides a way for other nodes to connect to them, and add them into a static-nodes.json file to be placed in the node1/geth folder, an example of which is shown below:

![static-nodes](https://user-images.githubusercontent.com/20734215/139522693-69094af2-718b-4066-bc46-478e53181900.PNG)

    
chain_setup can assist in getting the enode number, through selecting option 4 (List your enode id)
    
![List_Enode_ID](https://user-images.githubusercontent.com/20734215/139522191-47a7a63e-a00d-488c-b2ac-735a3fd83ee2.PNG)
    
A sample static-nodes.json file looks like this:
    
```
[
  "enode://xxxxx@ip1:port1",
  "enode://yyyyy@ip2:port2"
]
```
    
After creating and placing the static-nodes.json file in the node1/geth folder, restart your node.

*Note: The above steps must be performed for every single node in the network, so they can find one another*


#### Verifying that each node can see the other nodes
Verify that you are connected to the rest of the nodes by running chain_setup, and entering option 3 (List nodes you are connected to)
    
![List_Connected_Nodes](https://user-images.githubusercontent.com/20734215/139522293-0c7c3f76-ef20-4899-bd8c-8981c8be9029.PNG)

If you don't see all the nodes that are supposed to be in your network, check your static-nodes.json file in the previous step, or if that fails run the actual geth command from the chain_setup file directly in the console with verbosity 5, and observe the output for errors.

```
geth --datadir node1 --syncmode full --port xxxxx --nat extip:10.7.0.x --netrestrict 10.7.0.0/24 --http --http.addr 10.7.0.x --http.port 85xx --http.api personal,eth,net,web3 --http.corsdomain '*' --networkid xxxx --miner.gasprice 0 --unlock '0x12345678' --password node1/password.txt --mine --allow-insecure-unlock --miner.gaslimit 15000000 --nodiscover --verbosity 5
```

### Using the brownie and web3.py APIs

#### Connecting to the ByteABlock Network
To connect our nodes to the ethereum python APIs, so as to perform actions on the blockchain, we need to perform the below steps:

1) Create a new brownie project
    `mkdir brownie && cd brownie && brownie init`
2) Then tell brownie about the network we created earlier

    `brownie networks add live byteablock host=http://10.7.0.x:xxxx chainid=xxxx name="ByteABlock Network"`
    
3) Go back to the main project folder, whatever you have named it, and then run demo.py, which contains commented examples as to how to use the APIs

#### Deploying a contract
To deploy a contract, first ensure that the contract ByteABlock.sol is in the brownie contracts folder first (ie ByteABlock/brownie/contracts)

Then call the `deploy_and_get_abi()` helper function in demo.py while connected to the network. 
More details of connecting to the network can be found in demo.py

Finally note down where the contract is deployed to, so we can get the contract in the future.

*Sample of test contract deployment*

![ByteABlock Deploy](https://user-images.githubusercontent.com/20734215/139530925-d5811b5c-5134-473c-8cd7-eccddb064fa3.PNG)
    
 
 ### Web Server Prerequisites
1) Python 3.7.5    
2) MYSQL Server
3) MYSQL Workbench    
4) pip3 install requirements.txt 
5) Install the prerequisites of chain_dev
6) Execute the "forensic_blockchain.sql" file in MySQL Workbench and it will create 2 different tables (account & bitcase)
7) Change/modify the settings as shown in the app.py file accordingly. We have set up a cloud server as the mobile app needs to be able to interface to the web application and the blockchain. 
 
![image](https://user-images.githubusercontent.com/41332404/140599518-e1caf316-c2d9-4c8b-8abd-3769c2cce287.png)

### How to run
You can run the web application by running this command “python3.7 app.py” and to access the URL as shown below respectively. 
![image](https://user-images.githubusercontent.com/41332404/140599552-a4d38f12-ddd1-4fb9-9206-d98bceb8736b.png)

    
### Features of the web application
This section describes all the respective pages in the web application as well as the functionalities. 
    
![CAPTURE](https://user-images.githubusercontent.com/41332404/140614854-48d4c70b-2ff6-4aa1-ad1e-705e7e8789b8.png)
   
    */register page*
You will first need to register for an account before being authorized to access the web application. Upon successful registration, it will send a verification email to your email address which you will need to verify before being able to use it. 
    
![Capture](https://user-images.githubusercontent.com/41332404/140615026-1315cf30-df6b-45c8-a0b3-c32274d73a54.PNG)
    
     */Email Account activation*

![Capture](https://user-images.githubusercontent.com/41332404/140615065-78f52640-19ae-4790-836e-427d4c74ce50.PNG)

     */forgotpassword *
This page allows the investigator to reset their password if they forget their password by entering their email. If the account/email is valid, the investigator should be able to receive the following email to reset their password.

![Capture](https://user-images.githubusercontent.com/41332404/140615094-ef34e4c1-9894-429f-b244-2e94f8b1b931.PNG)
    
The investigator then can reset his/her password by entering a new password and it will direct him to the login page if there is no error. 

![Capture2](https://user-images.githubusercontent.com/41332404/140615720-d4b70359-ba49-4b7a-b89c-b5489027badf.PNG)

![2021-11-06_23-51-44](https://user-images.githubusercontent.com/41332404/140615648-eebcc43c-422d-4abf-9743-3fbc971cfad8.png)

    
    */Index page*

This is the login page where the investigator can access the web application with the correct credentials. 
    
![2021-11-06_23-56-17](https://user-images.githubusercontent.com/41332404/140615822-c0096f75-a519-43dd-aa3e-cf218130268d.png)

    
      */Home (Logged in with admin account)*
 
This is the dashboard page where it outputs the name of the investigator, role/privileges that the investigator has, number of cases the user has and the latest 5 transactions to the blockchain such as any new statusChanged or evidenceAdded.  
    
![Capture](https://user-images.githubusercontent.com/41332404/140615862-cda06bc9-551e-4f89-942a-db6d4afd7963.PNG)
  
    */Home (Logged in with member account)*
    
When logged in with a higher privilege account(admin), you will be able to see the latest 5 transactions to the blockchain for all the cases. However, with a lower privilege account, you will only be able to see the latest 5 transactions to the blockchain for the cases that you oversee. This explains the reason for the empty table as the user does not have any cases.
    

![Capture](https://user-images.githubusercontent.com/41332404/140616103-f542ea6b-6266-40cf-bfee-86c2a4b592a6.PNG)

 
    */Profile*

On the profile page, the investigator can only view their account details such as username, email & role. 
    

![2021-11-07_0-07-52](https://user-images.githubusercontent.com/41332404/140616162-1ffbe118-2f14-4dbd-82c9-6f248475ff9d.png)
    
    
    */Edit_Profile*
    
Investigators can choose to edit the account details such as changing the username, password & email.
  
 
![Capture](https://user-images.githubusercontent.com/41332404/140616284-69e6283e-ca74-4919-b4ca-312af28a4ae3.PNG)


     */Case*
    
Investigators can view all the case details that they are assigned to such as the case ID, case name, date, assigned_to, location, status, and evidence. To view the evidence of each case, the investigator would have to click the view button. 
    
    

![image](https://user-images.githubusercontent.com/41332404/140616736-738df143-fcea-47b9-ad1e-c28c7c37678e.png)


    
     */Show_Case*
    
Upon clicking the view evidence button, the show_case page shows a list of evidence that the case contains such as the handler, location, Image_Hash, Evidence Type, Serial Number, Model, Status, Purpose, Notes, Time. 
    
    
    
![Capture](https://user-images.githubusercontent.com/41332404/140616612-1b8877f3-fb00-4641-9acc-4bf1527f0faa.PNG)

 
     */evidence_history*
    
To view the check-in/check-out history of the evidence, we can click “show evidence history” where gives us the evidence timeline.
  

 
![Capture](https://user-images.githubusercontent.com/41332404/140616842-c3c7a2ae-61c5-40de-87ea-b8c4e668c624.PNG)
 
    
     */Case_Add*
    
    
Investigator can create a new case and it will be populated to the database. 



![Capture](https://user-images.githubusercontent.com/41332404/140616908-a9a92919-a8a7-4ebf-b851-88695882d387.PNG)

   
      */Admin*

Investigators can only access the admin portal if their account role is set to “admin”. The first page of the admin portal allows the investigator to view all the account details registered in the web application.
    
    
    
    
![Capture](https://user-images.githubusercontent.com/41332404/140616936-a4c027d5-7bde-4487-86d5-1216ac1f0f20.PNG)

    
     */Admin/Account*
 
The second page of the admin portal allows the investigator to add new accounts. 
    
    
    
 ![Capture](https://user-images.githubusercontent.com/41332404/140616996-8e6b6bde-0cc1-4b59-90da-83240d198c86.PNG)

    
    */Admin/case*
 
The third page of the admin portal allows the investigator to view & edit all case details including those that are not owned by the admin.
    
    

 ![Capture](https://user-images.githubusercontent.com/41332404/140617024-2af77c54-bd55-42b2-907b-1e7f090eb704.PNG)

  

    */Admin/editcase*
    
    
![Capture](https://user-images.githubusercontent.com/41332404/140617044-6a789429-5736-4864-bde4-b28388ae0fab.PNG)
    
    
    */Admin/evidence*
    
    
The last page of the admin portal allows the investigator to view all the transaction details/activity in the blockchain as shown in the image.


    

    




