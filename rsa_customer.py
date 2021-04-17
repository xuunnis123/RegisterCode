"""
To validate Code
"""
import datetime
import base64
import os
import json
from argparse import ArgumentParser
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

def check_key(en_code):
    """
    Check Key is valid
    """
    if en_code!='':
        print("code=", en_code)
        code = en_code[0:4]
        code+= '-'
        code+= en_code[4:6]
        code+= '-'
        code+= en_code[6:8]
        today = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        machine = en_code[8:]
        if machine==str(gma()):

            #code1='2021-04-20'
            if code >= today:
                return True
            else:return "EXPIRED CODE"
        else:return "Error: On Different Device."
    else:return "MISSING CODE"

def decode_rsa(encode):
    """
    decoded by RSA
    """
    print(encode)
    encode = encode.encode("UTF-8")
    encode = base64.b64decode(encode)
    encode = encode.decode("UTF-8")
    signature = encode
    buffer = signature.split("_")
    print(buffer)
    message_verify = buffer[0]
    signature = buffer[1]
    content = buffer[2]
    rsakey = RSA.importKey(open("public.pem").read())
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    hsmsg = SHA.new()
    hsmsg.update(message_verify.encode("utf-8"))

    is_verify = verifier.verify(hsmsg, base64.b64decode(signature))
    if is_verify is True:
        print("is_verify:",content)
        return content
    else: return is_verify


def check_authfile():
    """
    Check auth-file
    """
    with open('licensefile.skm', 'r') as file_content:
        save = json.loads(file_content.read())
        if save['encode']!='':
            return save['encode']
        else: return "Error Code."



def execute():
    """
    Execute this app
    """
    flag = False
    #### basic info.####
    filepath = os.getcwd()+"/licensefile.skm"
    if os.path.isfile(filepath) is False:
        return "Do not Exist File."
    record_code = check_authfile()
    record_code = decode_rsa(record_code)
    #record_code = record_code.encode("UTF-8")
    #ecord_code = base64.b64decode(record_code)
    #record_code = record_code.decode("UTF-8")
    result = check_key(record_code)
    if result is True:
        flag = True
    else:
        print(result)
        print("execute again")
        #os.remove("licensefile.skm")
     
    return flag

if __name__ == '__main__':

    if execute() is True:
        print("Continue")
    else:print("Cannot Validate!!")
    