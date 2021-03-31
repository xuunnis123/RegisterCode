import datetime
import platform
from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex
import base64
import os
def keyGen(key,machineCode,date,iv,mode):
    '''
    編碼的原理去製作的
    一般來說 就是把編碼後"認證碼"給使用者去輸入
    Base32 會輸出26各字 看起來會很不對稱
    這個時候 很多程式會多加兩個字(ex:JS)
    讓整個碼變成4*7 =28各字 變得比較對稱
    EX: "DYWS YQK7 V25E YA6M 3G8M HXNY CN"
    "DYWS YQK7 V25E YA6M 3G8M HXNY CNJS"
    '''
    code=date
    code=code.encode('utf-8')
    en_code = encryp_str(code, key, mode, iv)
    
    return en_code

def formatCode(en_code):
    encode32=base64.b32encode(en_code.encode())
    print(encode32)
    return encode32

def deFormat(de_code):
    de_code
    return de_code

def checkKey(en_code,key,mode,iv):
    #把暗碼解成明碼
    try:
        de_code=decryp_str(en_code,key,mode,iv)
    except:
        return "Some Error" 
        
    if de_code!='':
        code=de_code[0:4]
        code+='-'
        code+=de_code[4:6]
        code+='-'
        code+=de_code[6:]
        today=str(datetime.datetime.today().strftime("%Y-%m-%d"))
        
        #code1='2021-04-20'
        if code>=today:
            return True
        else:return False
    else: return False
    
    

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
    content = bytes.decode(content).rstrip('\0')
    print('明文：', content)
    return content

if __name__ == '__main__':
    date=datetime.datetime.today().strftime("%Y%m%d")
    machineCode=str(getMachineCode())
    key="testkey"
    while len(key)%16!=0:
        key+='\0'
    key=key.encode('utf-8')
    iv = os.urandom(16) #使用密碼學安全的隨機方法os.urandom
    #iv="16" #偏移量
    #iv=iv.encode('utf-8')
    mode = AES.MODE_CBC  # 加密模式

    en_code=keyGen(key,machineCode,date,iv,mode)
    print("en_code=",en_code)

    test=checkKey(en_code, key, mode, iv)
    print("test=",test)
