from base64 import urlsafe_b64decode, urlsafe_b64encode
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

from components.constants import Const


def int_to_bytes(number: int) -> str:
    return urlsafe_b64encode(bytearray.fromhex('{:064x}'.format(int(number)))).decode()


def bytes_to_int(number: str) -> int:
    return int(urlsafe_b64decode(number + "=").hex(), 16)


def pad_key(key: str) -> str:
    key = key.encode() + b".listrum"
    hash = SHA256.new(key).digest()

    return urlsafe_b64encode(hash).decode()[:Const.pad_length]


def import_pub(key: ECC.EccKey):
    key = urlsafe_b64encode(
        key.public_key().export_key(format="DER")).decode()

    owner = pad_key(key)
    return key, owner


def verify(key: str, data: str, sign: str) -> bool:
    # print(key, data, sign)
    key = ECC.import_key(urlsafe_b64decode(key))
    sign = urlsafe_b64decode(sign)

    DSS.new(
        key, 'fips-186-3').verify(SHA256.new(data.encode()), sign)


def test() -> None:
    key = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEQsFzkGckNAheZnYHolx3uQ7go8-lfHxIDU0O-fWTkXww7Zwjnt3DP79ucX2CwVsOPyUFLfJxWMC7hLBkqVXydg=="
    signature = "4zHzFP5E1xM99cnc4dNrJq6Q-MnOQdVJobkLPYtPMRFePCoWGy752b6wBsZ18qWDY4MdgPcgnOfMHmcZSJ_-ww=="
    data = "123"

    res = verify(key, data, signature)
    assert(res)
    print("ECDSA test passed")
