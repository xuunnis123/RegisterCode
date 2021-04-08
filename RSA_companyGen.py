
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




def keyGen(key,machineCode,date,iv,mode):

    code=date
    code+=machineCode
    print(code)
    code=code.encode('utf-8')
    en_code = encryp_str(code, key, mode, iv)
    print(type(iv),type(en_code))
    print("iv=",iv)
    encode=hexlify(iv).decode()+"_"+en_code
    print("encode=",encode)
    return encode


def generatePrivatePublic():
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    privateKey=key.exportKey()
    with open("private.pem", "wb") as f:
        f.write(privateKey)

    
    publicKey=key.publickey().exportKey()
    with open("public.pem", "wb") as f:
        f.write(publicKey)
    
    # 讀取 RSA 金鑰
    encodedKey = open("private.pem", "rb").read()

    # 解密 RSA 金鑰
    key = RSA.import_key(encodedKey)

    # 輸出 RSA 私鑰
   
    public=open("public.pem").read() #string
    private=open("private.pem").read()
    
    return public,private

    


def encode_RSA(content,public):
    #encode
    publicKey = RSA.import_key(public)

    sessionKey = get_random_bytes(16) #AES Session
    # 以 RSA 金鑰加密 Session 金鑰
    cipherRSA = PKCS1_OAEP.new(publicKey)
    encSessionKey = cipherRSA.encrypt(sessionKey)

    # 以 AES Session 金鑰加密資料
    cipherAES = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipherAES.encrypt_and_digest(bytes(content,encoding='utf8'))
 
    return encSessionKey,cipherAES.nonce,tag,ciphertext

def decode_RSA(encode):
    #decode

    encode=base64.b64decode(encode)
  
    enc=()
    for _ in encode.decode().strip().split(","):
        enc=enc+(_,)
    encode=enc
    print(encode)
    '''

    encode[0]:encSessionKey,
    encode[1]:cipherAES.nonce,
    encode[2]:tag,
    encode[3]:ciphertext
    encode[4]:privateKey
    '''
    # 讀取 RSA 私鑰
    private=encode[4]
    privateKey = RSA.import_key(private) 
    # 以 RSA 金鑰解密 Session 金鑰
    cipherRSA = PKCS1_OAEP.new(privateKey)
    sessionKey = cipherRSA.decrypt(encode[0])
    # 以 AES Session 金鑰解密資料
    cipherAES = AES.new(sessionKey, AES.MODE_EAX, encode[1])
    data = cipherAES.decrypt_and_verify(encode[3], encode[2])
    print(data.decode("utf-8"))

def formatCode(key):
    while len(key)%16!=0:
        key+='\0'
    key=key.encode('utf-8')
    return key

def generateEncodeFile(en_code,machineCode,date):
    data={'encode':en_code,'machineCode':machineCode,'ExpiredDate':date}
    filename=machineCode
    with open(filename+'.json', 'w') as f:
        json.dump(data,f)

if __name__ == '__main__':
   from argparse import ArgumentParser
   parser = ArgumentParser()
    #parser.add_argument("-a", "--inputA", help="this is parameter a", dest="argA", type=int, default="0")
   parser.add_argument('-machineCode',help='machineCode',dest="machineCode")
   parser.add_argument('-date', help='Valid date(yyyymmdd)',dest="date")
    #parser.add_argument('-code',help='Input your code',dest="code")
   args = parser.parse_args()
   #date=datetime.datetime.today().strftime("%Y%m%d")

   date="20210408"
   #date = args.date
   #machineCode=args.machineCode
   machineCode="34:c9:3d:47:94:a6"

 
   key="testkey"
   key=formatCode(key) 
   iv = os.urandom(16) #使用密碼學安全的隨機方法os.urandom
   #print("com_iv=",iv)
   mode = AES.MODE_CBC  # 加密模式

   #en_code=keyGen(key,machineCode,date,iv,mode) 
   #generateEncodeFile(en_code,machineCode,date)

   public,private=generatePrivatePublic()
   
   code=date
   code+=machineCode
   
   encode=encode_RSA(code,public)
   encode=encode+(private,)
   for _ in encode:
       if type(_) == str:
            continue
       else:
            bytes.decode(_)
   
   
   #Base64 Encode
   encode=base64.b64encode(str(encode).encode("utf-8"))
   #decode_RSA(encode)
   '''
   generateEncodeFile(encode,machineCode,date)
   cipher = PKCS1_cipher.new(keys)
   print("keys:",pubkeystr,privkeystr)
   #print(cipher.decrypt(base64.b64decode(encode), 0).decode('utf-8'))
   encode=privkeystr.decode('utf-8')+"_"+encode
   print(encode) 
   '''
   
