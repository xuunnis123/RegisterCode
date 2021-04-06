import datetime
import platform
from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex,unhexlify
import base64
import os
import string
import random
import json
from cryptography.fernet import Fernet
import codecs
from companyGenKey import keyGen
import logging

def checkKey(en_code,key,mode,iv):
    #把暗碼解成明碼
    print("checkKey")
    print(en_code,key,mode,iv)
    try:
        de_code=decryp_str(en_code,key,mode,iv)
    except:
        print("except")
        return en_code 
    print("de_code="+de_code)    
    if de_code!='':
        print("code=",de_code)
        code=de_code[0:4]
        code+='-'
        code+=de_code[4:6]
        code+='-'
        code+=de_code[6:8]
        today=str(datetime.datetime.today().strftime("%Y-%m-%d"))
        machine=de_code[8:]
        if machine==str(getMachineCode()):

            #code1='2021-04-20'
            if code>=today:
                return True
            else:return "EXPIRED CODE"
        else: return "Error: On Different Device."
    else: return "MISSING CODE"
    
    

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

def decryp_str(en_content, key, mode, iv):
    cryptor = AES.new(key, mode, iv)
    content = a2b_hex(en_content)
    print('解密1：', content)
    content = cryptor.decrypt(content)
    print('解密2：', content)
    print("content=",content)
    content = bytes.decode(content).rstrip('\0')
    print('明文：', content)
    return content

def generateAuthFile(en_code,machineCode):
    data={'encode':en_code}

    with open('licensefile.skm', 'w') as f:
        json.dump(data,f)

def checkAuthFile():
    
    
    with open('licensefile.skm', 'r') as f:
        save=json.loads(f.read())
        if save['encode']!='':
            return save['encode']
        else: return "Error Code."
        

def formatCode(key):
    while len(key)%16!=0:
        key+='\0'
    key=key.encode('utf-8')
    return key

def inputCode(machineCode):
    en_code=input('Input your code:')
    generateAuthFile(en_code,machineCode)

def execute():
    flag=False
    #### basic info.####
    
    machineCode=str(getMachineCode())
    key="testkey"
    key=formatCode(key)
    '''
    {"encode": "77065fd24a7e1f1ab0966f5b8c7c823a|1e842f11b9e61fb6b59fb3741f0587300653158c73c20c7ecfd54d9e6e5374021691497eeeef8ac97901bc19935916f0ae4b63f9475906639539b6441114482c", "machineCode": "ezra-HP-Pavilion-Gaming-Laptop-17-cd1xxx", "ExpiredDate": "20210406"}

    '''
    
    mode = AES.MODE_CBC  # 加密模式
    filepath=os.getcwd()+"/licensefile.skm"

    if os.path.isfile(filepath)==False:
        # generate code
        print("Gen")
        inputCode(machineCode)
        #en_code=input('Input your code:')
        #generateAuthFile(en_code,machineCode)
        # check code
    #iv = os.urandom(16) #使用密碼學安全的隨機方法os.urandom
    recordCode=checkAuthFile()
    iv=unhexlify(recordCode.split('|',1)[0])
    record=recordCode.split('|',1)[1]
   
    result=checkKey(record, key, mode, iv)
 
    if result==True:
            flag=True
    else:
        print(result)
        inputCode(machineCode)
        execute()

    return flag

if __name__ == '__main__':
    
    if execute() == True:
        print("Continue")
    else:print("Cannot Validate!!")

    
    
    









