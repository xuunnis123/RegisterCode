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
                return "EXPIRED CODE"
        else:
            return "Error: On Different Device."
    else:
        return "MISSING CODE"


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

    print("is_verify:", is_verify)
    if is_verify is True:
        print("is_verify:", content)
        return content
    else:
        return is_verify


def check_authfile():
    """
    Check auth-file
    """
    with open('licensefile.skm', 'r') as file_content:
        save = file_content.read()
        if save != '':
            return save
        else:
            return "Error Code."


def execute():
    """
    Execute this app
    """
    flag = False
    filepath = os.getcwd()+"/licensefile.skm"
    if os.path.isfile(filepath) is False:
        return "Do not Exist File."
    record_code = check_authfile()
    record_code = decode_rsa(record_code)
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
    else:
        print("Cannot Validate!!")
