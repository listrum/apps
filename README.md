# [Client](https://github.com/listrum/main#client) | [Node](https://github.com/listrum/main#node) | [Networking](https://github.com/listrum/main#networking) | [Glossary](https://github.com/listrum/main#glossary)
## Running listrum
**Requirements**: python3, pip, domain with an SSL certificate

- Installing python package:
>`pip install listrum -U`

- Starting a node:
>`python3 -m listrum.node`
Setup node_config.json in your home dir and start again

## Client

### Client class API
	Client(key: dict = {}) - use plain JWK from browser or generates new
	send_all(to: str) - sends all funds to wallet address
	balance() -> float - balance of imported key
	wallet: str - get padded wallet address
	
### Making apps:
	from listrum.client import Client

	cash = Client(req["cash_key"])
	cash.withdraw(1)
	
	print("Success")

## Node

### Node Config:

Stored in your home user directory in /listrum/node_config.json

	{
		"port": 2525,
		"wallet": your wallet for app payments and issue
		"cert": full path to SSL sertificate
		"cert_key": full path to SSL private key
	}
	
### Node commands:
- /issue Value - add value to your wallet
- /q - close node
- /update - update your nodes list 

### Node class API
	on_send(Tx) - called on successfull tx
	on_request(Request) - called on request
	
### Node apps:
Start all apps with
> `python3 -m listrum.apps`

Launchaing app example:
	from listrum.node import Node, Request
	from listrum.node.tx import Tx
	
	def on_request(req: Request) -> None:
		on_buy(req)
		
	def log(tx: Tx) -> None:
		print(tx.params)	
	
	node = Node()
	node.on_request = on_request
	node.on_send = log

## Glossary:
### Nodes:
- **trusted_nodes** - nodes your node will ask for unknown balances
- **broadcast_nodes** - nodes where tx will be broadcasted (auto for trusted nodes)
- **storage** - store wallets' balance in home dir /listrum/storage

### Wallets:
- **pad_length** - short public key length

### Transactions:
- **Repay** - amount of value payed back to sender
- **Fee** - difference between sended and received value
- **tx_ttl** - time tx will be stored until timestamp invalid
- **fee** - present of sended value that will be received
- **repay_update** - time after repay value will be updated
- **repay_value** - present of all repay value per transaction 

### Cash:
Send an amount to temporary wallet and send their private key 


## Networking:

### Balance:
	HTTPS GET :2525/balance/WalletAddress
	
	200 OK balance 

### Send:
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

### Get fee
	HTTPS GET :2525/fee

	200 OK Fee
