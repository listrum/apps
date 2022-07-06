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
- **Node list** - interact with other nodes
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
- /issue Value Address - add value to address
- /clear - remove all nodes

## Working with client
**Requirements**: python3, pip

- Installing python package:
>`pip install listrum`

- (Optional) Starting console client:
>`python3 -m listrum.client`

### Commands:
- /list - list all connected nodes
- /add Node - add node to node list
- /remove Node - remove node from node list
- /clear - remove all nodes
- /balance - show balance and wallet address
- /priv - export private key
- /history (SourceNode) - show history of your wallet

### API:
	 Client(priv_key: str= "")
	 self.key - wallet address
	 self.nodes - integrate with nodes: send(), balance()
	 export_priv() -> str

### Glossary:
- **self.owner** - full public key
- **self.key** - compressed wallet key
- **export_priv()** - export for browser and client
- **Nodes** - interactive nodes list class with all methods

## Network interface
#### Balance:
	HTTPS GET /balance/WalletAddress
	200 OK balance 

#### Send:
	HTTPS GET /send/
	{
		"from": {
			"owner": FullWalletAddress,
			"time": Timestamp,
			"sign": sign(to + time)
		},
		"data": {
			"to": WalletAddress,
			"value": FloatValue
		}
	}
	
	200 AddedValue

#### History:
	HTTPS GET /history/WalletAddress
	
	200 OK [{"to": WalletAddress, "value": FloatValue}, ..]
