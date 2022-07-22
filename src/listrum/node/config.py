import json
import os


path = os.path.expanduser("~") + "/listrum/"

try:
    os.makedirs(path)
except:
    pass

try:
    open(path + "node_config.json")
except:

    f = open(path + "node_config.json", "w")
    f.write(json.dumps({
        "port": 2525,
        "wallet": "HB44CTeu-57gm8gw4",
        "cert": "/home/me/keys/fullchain.pem",
        "cert_key": "/home/me/keys/privkey.pem",
        "tx_ttl": 2000,
        "pad_length": 17,
        "fee": 0.998,
        "repay_update": 30*1000,
        "repay_value": 0.01,
        "temp_storage_len": 10
    }))
    f.close()

f = open(path + "node_config.json")
config = json.loads(f.read())

port = config["port"]
wallet = config["wallet"]
cert = config["cert"]
cert_key = config["cert_key"]
tx_ttl = config["tx_ttl"]
pad_length = config["pad_length"]
fee = config["fee"]
repay_update = config["repay_update"]
repay_value = config["repay_value"]
temp_storage_len = config["temp_storage_len"]
