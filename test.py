import os
#import wmi
import platform
import uuid
import sys  
from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex
import string
from random import uniform, random, choice, sample

class Ctypto:
    
    def length(value):
        l = len(value)
        flag = l % 16
        if flag != 0:
            add = 16 - (l % 16)
            value = value + ('\0' * add).encode('utf-8')
        return value


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
        print('加密1：', cipher_content)
        cipher_content_hex = b2a_hex(cipher_content)
        print('加密2：', cipher_content_hex)
        cipher_content_hex_de = cipher_content_hex.decode()
        print('密文：', cipher_content_hex_de)
        return cipher_content_hex_de


    def decryp_str(en_content, key, mode, iv):
        cryptor = AES.new(key, mode, iv)
        content = a2b_hex(en_content)
        print('解密1：', content)
        content = cryptor.decrypt(content)
        print('解密2：', content)
        content = bytes.decode(content).rstrip('\0')
        print('明文：', content)
        return content


       
class Envinfo:
    
    def password(length):
        pw = str()
        characters = "qwertyuiopasdfghjklzxcvbnm" + "1234567890"
        pw=''.join(choice(string.ascii_uppercase) for x in range(length))
        return pw
    
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
class License:
    def IsOnRightMachine(license_key,):
        return true
    
    def 

'''
TEST_MACHINE="ezra-HP-Pavilion-Gaming-Laptop-17-cd1xxx"


if __name__ == '__main__':
    key = Envinfo.password(16) # secret key
    print("Key="+key)
    text = Envinfo.getMachineCode() #PUBLIC KEY
    content = text
    # 密钥
    #key = input(key)
    key = key.encode('utf-8')  
    # 偏移量
    
    iv="16" #偏移量
    print('原文：', content)
    content = content.encode('utf-8')  # 加密内容
    iv = iv.encode('utf-8')
    

    key = Ctypto.length(key)
    iv = Ctypto.length(iv)

    mode = AES.MODE_CBC  # 加密模式

    en_content = Ctypto.encryp_str(content, key, mode, iv)
    content = Ctypto.decryp_str(en_content, key, mode, iv)
