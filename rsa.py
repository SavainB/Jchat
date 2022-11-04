from random import *
from Crypto.Util.number import getPrime, inverse
from Crypto.Cipher import AES
from secrets import token_bytes
from hashlib import sha512
import hashlib

key_size = 32
keyok = token_bytes(16)

def gen_rsa_keypair(bits): # Génerer une clé
    pq_size = bits // 2 
    p = getPrime(pq_size)
    q = getPrime(pq_size)
    while p == q:
        p = getPrime(pq_size)
        q = getPrime(pq_size)
    n = p * q
    ph_n = (p - 1) * (q - 1)
    e = 65537
    assert(e < ph_n and ph_n % e != 0)
    d = inverse(e, ph_n)
    return ((e, n),(d, n))

def gen_aes_key():
    return AES.new().read(key_size)

def rsa(msg, key):
    var1 = pow(msg, key[0][0], key[0][1]);
    var2 = pow(msg, key[1][0], key[1][1]);
    return (var1, var2)
def rsatest(msg, key):
    var1 = pow(msg, key[0], key[1]);
    return (var1)

def rsa_enc(msg, key): # Chiffrement
    msg = int.from_bytes(msg.encode('UTF-8'), 'big')
    keye = rsatest(msg, key)
    return keye

def rsa_dectest(msg, key): # Déchiffrement
    msg = rsatest(msg[0], key)
    return msg[1].to_bytes((msg[1].bit_length() + 7) // 8, 'big').decode('UTF-8')

def rsa_dec(msg, key): # Déchiffrement
    msg = rsa(msg, key)
    return msg[1].to_bytes((msg[1].bit_length() + 7) // 8, 'big').decode('UTF-8')

if __name__ == '__main__' :
    key = (gen_rsa_keypair(256))
    public_key = (key[0][0],key[0][1]);
    private_key =(key[1][0],key[1][1]);
    enc = rsa_enc('il est fou ?', public_key)
    print(enc)
    dec = rsa_dec(enc, key)
    print(dec)
