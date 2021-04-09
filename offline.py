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

def activateCode():
    code = string.ascii_letters+string.digits #alphabet code
    codes = [''.join(random.choices(code,k=5)) for _ in range(4)] #there are 5 codes in one section, total:4 sections
    actCode = '-'.join(codes)
    print("actCode=",actCode)
    return actCode

def formatCode(key):
    while len(key)%16!=0:
        key+='\0'
    key=key.encode('utf-8')
    return key

def checkKey(en_code,key,mode,iv):
    #把暗碼解成明碼
    try:
        de_code=decryp_str(en_code,key,mode,iv)
    except:
        return en_code 
        
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
            else:return "INVALID CODE"
        else: return "Error: On Different Device."
    else: return "MISS CODE"
    
    

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


def decryp_str(en_content, key, mode, iv):
    cryptor = AES.new(key, mode, iv)
    content = a2b_hex(en_content)
    #print('解密1：', content)
    content = cryptor.decrypt(content)
    #print('解密2：', content)
    print("content=",content)
    content = bytes.decode(content).rstrip('\0')
    print('明文：', content)
    return content

def generateAuthFile(en_code,authCode,machineCode):
    data={'encode':en_code,'authCode':authCode}

    with open('licensefile.skm', 'w') as f:
        json.dump(data,f)

def checkAuthFile(code):
    
    if code!='':
        with open('licensefile.skm', 'r') as f:
            save=json.loads(f.read())
            if save['authCode']==code:
                return save['encode']
            else: return "Error Code."
        
    else: return "Error: Input Nothing."

def test():
    print("test")
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    #parser.add_argument("-a", "--inputA", help="this is parameter a", dest="argA", type=int, default="0")
    parser.add_argument('-machineCode',help='machineCode',dest="machineCode")
    parser.add_argument('-date', help='Valid date(yyyymmdd)',dest="date")
    parser.add_argument('-reset', help='Generate a pair of new keys',dest="reset")
     #parser.add_argument('-code',help='Input your code',dest="code")
    args = parser.parse_args()
    #date=datetime.datetime.today().strftime("%Y%m%d")
    #### basic info.####
    date=datetime.datetime.today().strftime("%Y%m%d")
    machineCode=str(getMachineCode())
    key="testkey"
    key=formatCode(key)
    
    iv = os.urandom(16) #使用密碼學安全的隨機方法os.urandom
    #iv="16" #偏移量
    #iv=iv.encode('utf-8')
    mode = AES.MODE_CBC  # 加密模式
    filepath=os.getcwd()+"/licensefile.skm"

    print(filepath)
    if os.path.isfile(filepath)==False:
        # generate code
        print("Gen")
        en_code=keyGen(key,machineCode,date,iv,mode)
        authCode=activateCode()
        generateAuthFile(en_code,authCode,machineCode)

    # check code
    code=input('Input your code:')
    recordCode=checkAuthFile(code)
    result=checkKey(recordCode, key, mode, iv)
    print("Result:",result)

    

    
