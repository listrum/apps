# [Run](https://github.com/listrum/node-client#running-a-node) / [Networking](https://github.com/listrum/node-client#node-interface) / [API](https://github.com/listrum/node-client#nodes-api)
## Running listrum
**Requirements**: python3, pip, domain with an SSL certificate

- Installing python package:
>`pip install listrum`

- Starting a node:
>`python3 -m listrum.node`

### Config:
	{
		"storage": "temp/storage", - Storage of balances
		"port": 2525,
		"wallet": "vNNMgYUdN_bgsQuE0", - your wallet for app payments
		"cert": "keys/fullchain.pem", - SSL sertificate
		"cert_key": "keys/privkey.pem", - SSL private key
		"node_connect": {
			"enabled": true, - connect to your nodes to broadcast txs
			"price": 1.0, - price of connection
			"prime": "listrum.com" - first node address, can be your
		},
		"history": {
			"enabled": true, - save history
			"path": "temp/history" - path to save history
		},
		"key_storage": {
			"enabled": true, - store user's keys, launch with key_storage.py
			"port": 2526,
			"path": "temp/key_storage",
			"price": 1.0
		}
	}

### Glossary:
- **Node list** - node list to send and get data from
- **Repay** - amount of value payed back to sender
- **Fee** - difference between sended and received value
- **History node** - node that saves txs and sends it with /history/
- **Key storage** - store wrapped keys remotely for a price labled by a name
- **tx_ttl** - time tx will be stored until timestamp invalid
- **pad_length** - short public key length
- **fee** - present of sended value that will be received
- **repay_update** - time after repay value will be updated
- **repay_value** - present of all repay value per transaction 
- **Connect node** - resend transactions to your node for a price
- **Primary node (connect node)** - node where you get balances, can be the same node

### Commands:
- /list - list all connected nodes
- /add Node - add node to node list
- /remove Node - remove node from node list
- /issue Value Address - add value to address
- /clear - remove all nodes
- /wallet - change your wallet for payable methods 

### Node interface:

#### Balance:
	HTTPS GET :2525/balance/WalletAddress
	200 OK balance 

#### Send:
	HTTPS GET :2525/send/
	{
		"from": {
			"pub": FullWalletAddress,
			"time": Timestamp,
			"sign": sign(to + time)
		},
		"data": {
			"to": WalletAddress,
			"value": FloatValue
		}
	}
	
	200 OK

### History node interface:
	HTTPS GET :2525/history/WalletAddress
	
	200 OK [{"to": WalletAddress, "value": FloatValue}, ..]

### Get fee
	HTTPS GET :2525/fee

	200 OK Fee

### Key storage interface:
#### Store your key:
	HTTPS GET :2522/store/
	{
		"from": PrivateKey,
		"data" {
			"key": [Key, WrappedPrivateKey],
			"name": KeyName
		}
	}

	200 OK

#### Get key:
	HTTPS GET :2522/get/KeyName

	200 OK [Key, WrappedPrivateKey]

### Connect node:
	HTTPS GET :2525/connect/
	{
		"from": PrivateKey,
		"data": NodeAddress,
	}

	200 OK

### Get app price
	HTTPS GET :2525/price

	200 OK Price

## Nodes API
	add_node(address: str)
	remove_node(address: str)
	clear()
	send(data) -> spend
	balance(padded_key)
	client(key: dict = {}) -> Client - client constructor with self nodes and JWK

## Client API
	Client(key: dict = {}) - use plain JWK from browser
	send_all(to: str) - sends all funds to address
	balance() -> float - balance of the key, with nodes provided
