import os
#import wmi
import platform
import uuid
import sys  
from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex
import string
from random import uniform, random, choice, sample
import mysql.connector
from mysql.connector import Error

class Db:
    def connection():
       

        try:
            # 連接 MySQL/MariaDB 資料庫
            connection = mysql.connector.connect(
                host='localhost:3307',          # 主機名稱
                database='officeguide_db', # 資料庫名稱
                user='root',        # 帳號
                password='123456')  # 密碼

            if connection.is_connected():

                # 顯示資料庫版本
                db_Info = connection.get_server_info()
                print("資料庫版本：", db_Info)

                # 顯示目前使用的資料庫
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("目前使用的資料庫：", record)

        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("資料庫連線已關閉")
class Key:
    def password(length):
        pw = str()
        characters = "qwertyuiopasdfghjklzxcvbnm" + "1234567890"
        pw=''.join(choice(string.ascii_uppercase) for x in range(length))
        return pw

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
    
    def createKey(product_id,machine_code):
        


        return token


    def activate(token,aes_public_key,product_id,machine_code):
        response=Response("","",0,"")
        try:
            response = Response.from_string(HelperMethods.send_request("key/activate", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "key":aes_public_key,\
                                                  "MachineCode":machine_code,\
                                                  "Sign":"True",\
                                                  "SignMethod":1}))
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")    
        
        pubkey = RSAPublicKey.from_string(rsa_pub_key)
        if response.result == 1:
            return (None, response.message)
        else:
            try:
                if HelperMethods.verify_signature(response, pubkey):
                    return (LicenseKey.from_response(response), response.message)
                else:
                    return (None, "The signature check failed.")
            except Exception:
                return (None, "The signature check failed.")    

class RSAPublicKey:
    
    def __init__(self, modulus, exponent):
        self.modulus = modulus
        self.exponent = exponent
        
    @staticmethod
    def from_string(rsaPubKeyString):
        """
        The rsaPubKeyString can be found at https://app.cryptolens.io/User/Security.
        It should be of the following format:
            <RSAKeyValue><Modulus>...</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>
        """
        rsaKey = xml.etree.ElementTree.fromstring(rsaPubKeyString)
        return RSAPublicKey(rsaKey.find('Modulus').text, rsaKey.find('Exponent').text)

class Envinfo:
    
    
    
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
    key = Key.password(16) # secret key
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
    

    key = Key.length(key)
    iv = Key.length(iv)

    mode = AES.MODE_CBC  # 加密模式

    en_content = Key.encryp_str(content, key, mode, iv)
    content = Key.decryp_str(en_content, key, mode, iv)


    Db.connection()
