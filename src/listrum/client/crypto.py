from base64 import urlsafe_b64decode, urlsafe_b64encode
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

from listrum.client.constants import Const


def int_to_bytes(number: int) -> str:
    return urlsafe_b64encode(bytearray.fromhex('{:064x}'.format(int(number)))).decode()


def bytes_to_int(number: str) -> int:
    return int(urlsafe_b64decode(number + "=").hex(), 16)


def pad_key(pub: str) -> str:
    pub = pub.encode() + b".listrum"
    hash = SHA256.new(pub).digest()

    return urlsafe_b64encode(hash).decode()[:Const.pad_length]


def import_pub(priv: ECC.EccKey):
    pub = urlsafe_b64encode(
        priv.public_key().export_key(format="DER")).decode()

    wallet = pad_key(pub)
    return pub, wallet


def verify(pub: str, data: str, sign: str) -> bool:
    # print(key, data, sign)
    pub = ECC.import_key(urlsafe_b64decode(pub))
    sign = urlsafe_b64decode(sign)

    DSS.new(
        pub, 'fips-186-3').verify(SHA256.new(data.encode()), sign)


def test() -> None:
    pub = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEQsFzkGckNAheZnYHolx3uQ7go8-lfHxIDU0O-fWTkXww7Zwjnt3DP79ucX2CwVsOPyUFLfJxWMC7hLBkqVXydg=="
    signature = "4zHzFP5E1xM99cnc4dNrJq6Q-MnOQdVJobkLPYtPMRFePCoWGy752b6wBsZ18qWDY4MdgPcgnOfMHmcZSJ_-ww=="
    data = "123"

    res = verify(pub, data, signature)
    assert(res)
    print("ECDSA test passed")
