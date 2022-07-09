# [Run](https://github.com/listrum/node-client#running-a-node) / [Networking](https://github.com/listrum/node-client#node-interface) / [API](https://github.com/listrum/node-client#nodes-api)
## Running listrum
**Requirements**: python3, pip, domain with an SSL certificate

- Installing python package:
>`pip install listrum`

- Starting a node:
>`python3 -m listrum.node`

- Starting a history node:
>`python3 -m listrum.history`

- Starting a key storage:
>`python3 -m listrum.key_storage`

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

### Commands:
- /list - list all connected nodes
- /add Node - add node to node list
- /remove Node - remove node from node list
- /issue Value Address - add value to address
- /clear - remove all nodes

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


## Nodes API
	add_node(address: str)
	remove_node(address: str)
	clear()
	send(data)
	balance(padded_key)
	client(key: dict = {}) -> Client - client constructor with self nodes and JWK

## Client API
	Client(key: dict = {}) - use plain JWK from browser
	send_add(to: str) - sends all funds to address
	balance() -> float - balance of the key, with nodes provided
