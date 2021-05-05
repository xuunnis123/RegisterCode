"""
To validate Code
"""
import datetime
import base64
import os
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5


def check_key(en_code):
    """
    Check Key is valid
    """
    if en_code != '':
        expired = en_code.split("_")[0]
        code = expired[0:4]
        code += '-'
        code += expired[4:6]
        code += '-'
        code += expired[6:8]
        today = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        machine = en_code.split("_")[1]

        code += '-'
        code += machine[4:6]
        code += '-'
        code += machine[6:8]
        local_machine = str(gma())
        local_machine = local_machine.upper().replace(":", "")
        if machine == local_machine:
            if code >= today:
                return True
            else:
                raise ValueError("EXPIRED CODE")

        else:
            raise ValueError("Error: On Different Device.")
            
    else:
        raise ValueError("MISSING CODE")
        


def decode_rsa(encode):
    """
    decoded by RSA
    """

    encode = encode.encode("UTF-8")
    encode = base64.b64decode(encode)

    save = encode.split(b"_")
    
    b_expired = save[0]
    b_mac_address = save[1]
    b_save = save[2:]
    b_signature = b''

    count = 0

    for _ in b_save:
        if count > 0:
            b_signature += b'_' + _
        else:
            b_signature += _
            count += 1

    expired = b_expired.decode("UTF-8")
    mac_address = b_mac_address.decode("UTF-8")

    content = expired + "_" + mac_address
    message_verify = b_expired + b"_" + b_mac_address
    rsakey = RSA.importKey(open("public.pem").read())
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    hsmsg = SHA.new()
    hsmsg.update(message_verify)

    is_verify = verifier.verify(hsmsg, b_signature)

    if is_verify is not True:
        raise ValueError
    return content

def check_authfile():
    """
    Check auth-file
    """
    with open('licensefile.skm', 'r') as file_content:
        save = file_content.read()
        if save == '':
            raise ValueError
        return save

def check_license():
    """
    Execute this app
    """
    filepath = os.getcwd()+"/licensefile.skm"
    try:
            if os.path.isfile(filepath) is False:
                raise FileNotFoundError()
        
            record_code = check_authfile()
            record_code = decode_rsa(record_code)
            result = check_key(record_code)
        except:
            return False
        if result is True:
            return True


if __name__ == '__main__':

    if check_license() is True:
        print("Continue")
    else:
        print("Cannot Validate!!")
