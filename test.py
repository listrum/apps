import shutil
import json
from secrets import randbits, token_hex
import time
from random import randbytes, randint
# from matplotlib import pyplot as plt
# import numpy as np
from hashlib import sha256, sha3_256
import base64
# from listrum_node import node
# from listrum_cli import cli
import os
from base64 import b85encode, urlsafe_b64encode, urlsafe_b64decode, b16encode
# import block_db
import zlib
import http
import socket
import requests
from threading import Thread
import urllib.parse
from client import Client
from utils.https import Request
import utils.https as https
from node import Node
import sys

# try:
#     os.rmdir("node")
# except:
#     pass

node = Node()
node.set_storage()
node.start("keys/fullchain.pem",
           "keys/privkey.pem")

cli.add_node(["listrum.com"])
node.owner = cli.key
# res = cli.issue(8)
# print(res.text)

res = cli.send("123", 1)
print(res.text)

input()
print(cli.balance())
