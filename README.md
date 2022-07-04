# [Node](https://github.com/listrum/node-client#running-a-node) / [Client](https://github.com/listrum/node-client#working-with-client) / [Networking](https://github.com/listrum/node-client#network-interface)
## Running a node
**Requirements**: python3, pip, domain with SSL certificate

- Installing python package:
>`pip install listrum`

- Starting a node:
>`python3 -m listrum.node`

- (Optional) Starting a history node:
>`python3 -m listrum.history`

### Glossary:
- **Download node** - if your node doesn't know the balance, it will ask this node
- **Node list** - where transactions will be broadcasted
- **Repay** - amount of value payed back to sender
- **Fee** - difference between sended and received value
- **History node** - node that saves txs and sends it with /history/
- **tx_ttl** - time tx will be stored until timestamp invalid
- **pad_length** - short public key length
- **fee** - present of sended value that will be received
- **repay_update** - time after repay value will be updated
- **repay_value** - present of all repay value per transaction 

### Commands:
- /list - list all connected nodes
- /add Node - add node to node list
- /remove Node - remove node from node list
- /download Node - set download node
- /owner Address - set owner address (for issue)

## Working with client
**Requirements**: python3, pip

- Installing python package:
`pip install listrum`

- (Optional) Starting console client:
`python3 -m listrum.client`

### Commands:
- /list - list all connected nodes
- /add Node - add node to node list
- /remove Node - remove node from node list
- /clear - remove all nodes
- /issue Value - send mint request
- /balance - show balance and wallet address
- /priv - export private key
- /history (SourceNode) - show history of your wallet

### API:
	 Client(priv_key: str= "")
	 self.key - wallet address
	 self.nodes - list<NodeReq>
	 add_node(address: str)
	 export_priv() -> str
	 remove_node(address: str)
	 add_node(address: str)
	 send(to: str, value: float)
	 issue(value: float)
	 balance() -> float

### Glossary:
- **self.owner** - full public key
- **self.key** - compressed wallet key
- **balance()** - get balance from all nodes and calcualte average
- **NodeReq** - interactive node class

## Network interface
#### Balance:
	HTTPS GET /balance/WalletAddress
	200 OK balance 
#### Issue:
	HTTPS GET /issue/
	{
		"from": {
			"owner": FullWalletAddress,
			"time": Timestamp,
			"sign": sign(value + time)
		},
		"value": FloatValue
	}
		
	200 OK
		
#### Send:
	HTTPS GET /send/
	{
		"from": {
			"owner": FullWalletAddress,
			"time": Timestamp,
			"sign": sign(to + time)
		},
		"to": {
			"to": WalletAddress,
			"value": FloatValue
		}
	}
	
	200 OK
#### History:
	HTTPS GET /history/WalletAddress
	
	200 OK [{"to": WalletAddress, "value": FloatValue}, ..]
