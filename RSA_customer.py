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
from argparse import ArgumentParser
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import SHA



def checkKey(en_code):
    #把暗碼解成明碼
   
    if en_code!='':
        print("code=",en_code)
        code=en_code[0:4]
        code+='-'
        code+=en_code[4:6]
        code+='-'
        code+=en_code[6:8]
        today=str(datetime.datetime.today().strftime("%Y-%m-%d"))
        machine=en_code[8:]
        if machine==str(gma()):

            #code1='2021-04-20'
            if code>=today:
                return True
            else:return "EXPIRED CODE"
        else: return "Error: On Different Device."
    else: return "MISSING CODE"
    


def decode_RSA(encode):
    print(encode)
    encode=encode.encode("UTF-8")
    encode=base64.b64decode(encode)
    encode=encode.decode("UTF-8")
    signature = encode
    buffer=signature.split("_")
    print(buffer)
    message_verify=buffer[0]
    signature=buffer[1]
    content=buffer[2]
    rsakey = RSA.importKey(open("public.pem").read())
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    hsmsg = SHA.new()
    hsmsg.update(message_verify.encode("utf-8"))

    is_verify = verifier.verify(hsmsg, base64.b64decode(signature))
    if is_verify == True:
        return content
    else: return is_verify

def generateAuthFile(en_code,machineCode):
    en_code=en_code.encode("utf-8")
    en_code = base64.b64encode(en_code)
    # Decoding the Base64 bytes to string
    en_code = en_code.decode("UTF-8")
    
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
    en_code=args.code
    #en_code=input("CODE=")
    en_code=decode_RSA(en_code)
 
    if en_code == False:
        return "Not Validated User"
    generateAuthFile(en_code,machineCode)

def execute():
    flag=False
    #### basic info.####

    machineCode=str(gma())
    
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
    recordCode=recordCode.encode("UTF-8")
    recordCode=base64.b64decode(recordCode)
    recordCode=recordCode.decode("UTF-8")
    
    result=checkKey(recordCode)
    
    if result==True:
            flag=True
    else:
        print(result)
        print("execute again")
        os.remove("licensefile.skm")
        #inputCode(machineCode)
        #execute()

    return flag


def test():
    #args.code()
    print("args")
    print(args.validate_code)

if __name__ == '__main__':
    
    parser = ArgumentParser()
   
    parser.add_argument('-code',help='Input code',dest="code")
    parser.add_argument('-test',action='store_const',const=test)
    parser.add_argument('-revalidate',dest="validate_code")
    #parser.add_argument('-inputcode',action='store_const',const=)
    args = parser.parse_args()

    if execute() == True:
        print("Continue")
    else:print("Cannot Validate!!")
    

    
    
    









