from base64 import urlsafe_b64decode, urlsafe_b64encode
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


def pad_key(key: str) -> str:
    key = key.encode() + b".listrum"
    hash = SHA256.new(key).digest()

    return urlsafe_b64encode(hash).decode()[:17]


def verify(key: str, data: str, sign: str) -> bool:
    print(key, data, sign)
    key = urlsafe_b64decode(key)

    key = ECC.import_key(key)

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
