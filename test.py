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
from utils.https import Request
import utils.https as https
from node import Node

try:
    os.mkdir('test')
except:
    pass

key = input("Key file: ")
print(key)

# node1 = Node()
# node2 = Node()

# node1.set_storage("listrum.com:2526", "test/node1")
# node2.set_storage("listrum.com", "test/node2")

# node1.set_owner("gO5qyZHrd17GlFsuH")
# node2.set_owner("gO5qyZHrd17GlFsuH")

# node1.start("keys/fullchain1.pem",
#             "keys/privkey1.pem")

# node2.start("keys/fullchain1.pem",
#             "keys/privkey1.pem", 2526)
