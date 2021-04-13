
import datetime
import platform
from binascii import b2a_hex, a2b_hex,hexlify
import base64
import os
import string
import random
import json
from cryptography.fernet import Fernet
import codecs
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import SHA



def generatePrivatePublic():
    random_generator = Random.new().read
    # 產生 2048 位元 RSA 金鑰
    key = RSA.generate(2048, random_generator)
    privateKey = key.exportKey()
    
    # 保護金鑰的密碼
    secretCode = "secret#code"


    # 以密碼加密保護 RSA 金鑰
    encryptedKey = key.export_key(passphrase=secretCode, pkcs=8,
                                protection="scryptAndAES128-CBC")

    # 將 RSA 金鑰寫入檔案
    with open("private.pem", "wb") as f:
        f.write(encryptedKey)
    
    
    publicKey=key.publickey().exportKey()
    with open("public.pem", "wb") as f:
        f.write(publicKey)


def encode_RSA(content,machineCode):
    #encode
    message = machineCode
    f = open("private.pem","rb")
    rsakey = RSA.importKey(f.read(),passphrase='secret#code')
    f.close()
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf-8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    
    encode = machineCode+"_"+signature.decode('utf-8')+"_"+content
    encode = encode.encode("utf-8")
    encode = base64.b64encode(encode)
    # Decoding the Base64 bytes to string
    encode = encode.decode("UTF-8")
    return encode

def decode_RSA(encode):
    encode = encode.encode("UTF-8")
    encode = base64.b64decode(encode)
    encode = encode.decode("UTF-8")
    signature = encode
    buffer = signature.split("_")
    message_verify = buffer[0]
    signature = buffer[1]
    content = buffer[2]
    rsakey = RSA.importKey(open("public.pem").read())
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    hsmsg = SHA.new()
    hsmsg.update(message_verify.encode("utf-8"))

    is_verify = verifier.verify(hsmsg, base64.b64decode(signature))
    if is_verify == True:
        return content
    else: return is_verify



if __name__ == '__main__':
   from argparse import ArgumentParser
   parser = ArgumentParser()
    #parser.add_argument("-a", "--inputA", help="this is parameter a", dest="argA", type=int, default="0")
   parser.add_argument('-generatePrivatePublic',help='Generate Private key and Public key',dest="generatePrivatePublic")
   parser.add_argument('-machineCode',help='machineCode',dest="machineCode")
   parser.add_argument('-date', help='Valid date(yyyymmdd)',dest="date")
   parser.add_argument('-reset', help='Generate a pair of new keys',dest="reset")
    #parser.add_argument('-code',help='Input your code',dest="code")
   args = parser.parse_args()
   #date=datetime.datetime.today().strftime("%Y%m%d")

   date="20210413"
   #date = args.date
   #machineCode = args.machineCode
   machineCode="34:c9:3d:47:94:a6"


   gen = input("Generate:(Y/N)")
   #gen=args.generatePrivatePublic
   if args.reset != '':
        generatePrivatePublic()
   
   code = date
   code+= machineCode
   print("code="+code)
   encode = encode_RSA(code,machineCode)
   
   #Base64 Encode
   #encode=base64.b64encode(str(encode).encode("utf-8"))
  
   print(encode)

