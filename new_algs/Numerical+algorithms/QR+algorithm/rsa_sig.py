from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import Crypto.Hash.MD5


def rsa_sign(plaintext, key, hash_algorithm=Crypto.Hash.MD5):
    """RSA 数字签名"""
    signer = PKCS1_v1_5.new(RSA.importKey(key))

    #hash算法必须要pycrypto库里的hash算法，不能直接用系统hashlib库，pycrypto是封装的hashlib
    hash_value = hash_algorithm.new(plaintext)
    return signer.sign(hash_value)


def rsa_verify(sign, plaintext, key, hash_algorithm=Crypto.Hash.MD5):
    """校验RSA 数字签名"""
    hash_value = hash_algorithm.new(plaintext)
    verifier = PKCS1_v1_5.new(RSA.importKey(key))
    return verifier.verify(hash_value, sign)

