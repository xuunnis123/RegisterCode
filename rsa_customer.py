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
        expired=en_code.split("_")[0]
        code = expired[0:4]
        code+= '-'
        code+= expired[4:6]
        code+= '-'
        code+= expired[6:8]
        today = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        machine = en_code.split("_")[1]
        
        mac_address = machine[0:4]
        code+= '-'
        code+= machine[4:6]
        code+= '-'
        code+= machine[6:8]
        local_machine=str(gma())
        local_machine = local_machine.upper().replace(":","")
        if machine==local_machine:

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
    
    encode = encode.encode("UTF-8")
    encode = base64.b64decode(encode)

    print(encode)
    save=encode.split(b"_")
    print("save=",save)
    b_expired=encode.split(b"_")[0]
    b_mac_address=encode.split(b"_")[1]
    b_signature=encode.split(b"_")[2:]
    
    print("b_signature=",b_signature)
    print("b_signature_type=",type(b_signature))
    expired = b_expired.decode("UTF-8")
    mac_address=b_mac_address.decode("UTF-8")
    print("macB=",type(b_mac_address))
    signature=b_signature.decode("UTF-8")
    content=expired+"_"+mac_address
    message_verify=b_expired+b"_"+b_mac_address
    print(expired)
    print(mac_address)
   
    rsakey = RSA.importKey(open("public.pem").read())
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    hsmsg = SHA.new()
    hsmsg.update(message_verify)
    print(hsmsg)
    print(b_signature)
    
    is_verify = verifier.verify(hsmsg, signature)
    
    print("is_verify:",is_verify)
    if is_verify is True:
        print("is_verify:",content)
        return content
    else: return is_verify


def check_authfile():
    """
    Check auth-file
    """
    with open('licensefile.skm', 'r') as file_content:
        save =file_content.read()
        if save!='':
            return save
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
    print(record_code)
    print("----")
    record_code = decode_rsa(record_code)
    print("++++")
    print(record_code)
    result = check_key(record_code)
    if result is True:
        flag = True
    else:
        print(result)
        print("execute again")
        
     
    return flag

if __name__ == '__main__':

    if execute() is True:
        print("Continue")
    else:print("Cannot Validate!!")
    