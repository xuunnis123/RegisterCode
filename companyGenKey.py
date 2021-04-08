import datetime
import platform
from Crypto.Cipher import AES  
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


def encryp_str(content, key, mode, iv):
        cryptor = AES.new(key, mode, iv)
        
        key_length = len(key)
        content_legth = len(content)
        if content_legth < key_length:
            add = key_length - content_legth
            content = content + ('\0' * add).encode('utf-8')
        elif content_legth > key_length:
            add = 16 - (content_legth % 16)
            content = content + ('\0' * add).encode('utf-8')
        cipher_content = cryptor.encrypt(content)  # 加密
        #print('加密1：', cipher_content)
        cipher_content_hex = b2a_hex(cipher_content)
        #print('加密2：', cipher_content_hex)
        cipher_content_hex_de = cipher_content_hex.decode()
        print('密文：', cipher_content_hex_de)
        return cipher_content_hex_de

def formatCode(key):
    while len(key)%16!=0:
        key+='\0'
    key=key.encode('utf-8')
    return key
'''
def getMachineCode(v=1):
    if "windows" in platform.platform().lower():
        return platform.node()
    elif "mac" in platform.platform().lower() or "darwin" in platform.platform().lower():               
        res = platform.node()
        return platform.node()
    elif "linux" in platform.platform().lower() :
        return platform.node()
    else:
        return platform.node()
'''

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

   #date="20210407"
   date = args.date
   machineCode=args.machineCode
   #machineCode="34:c9:3d:47:94:a6"

 
   key="testkey"
   key=formatCode(key) 
   iv = os.urandom(16) #使用密碼學安全的隨機方法os.urandom
   #print("com_iv=",iv)
   mode = AES.MODE_CBC  # 加密模式

   en_code=keyGen(key,machineCode,date,iv,mode) 
   generateEncodeFile(en_code,machineCode,date)

   