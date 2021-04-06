import datetime
import platform
from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex
import base64
import os
import string
import random
import json
from cryptography.fernet import Fernet
import codecs

def keyGen(key,machineCode,date,iv,mode):

    code=date
    code+=machineCode
    print(code)
    code=code.encode('utf-8')
    en_code = encryp_str(code, key, mode, iv)
    
    return en_code


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

   #date=datetime.datetime.today().strftime("%Y%m%d")
   date="20210406"
   machineCode="ezra-HP-Pavilion-Gaming-Laptop-17-cd1xxx"
   #machineCode=input("machine Code:")
   #date=input("Expire Date:(yyyymmdd)")
   key="testkey"
   key=formatCode(key) 
   iv = os.urandom(16) #使用密碼學安全的隨機方法os.urandom
   mode = AES.MODE_CBC  # 加密模式

   en_code=keyGen(key,machineCode,date,iv,mode) 
   generateEncodeFile(en_code,machineCode,date)
   print(en_code)