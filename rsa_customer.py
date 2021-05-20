"""
To validate Code
"""
import datetime
import base64
import os
from machine_code import get_machine_code
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5


PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo7Cf19ho7hVAWRKuRIAa
kJ7tOw4JR6DqAD/ysgZCRqhl4wk4CocC5sKrk0Zx7NaWwDS8i4lXRTPuctlCr5SP
kAJzgVjONx++wZebmPwWWAvxtA01MoD+lzR+aJLeyPJfxDxZq7BwIu4tVamvE8aJ
7fTQOc8VOKWdCzyycpbOBKrNziIXW4HQ/A+gVuF+tiGp2H/+RiWTi1o+ftXJvDNV
E1duC1Xuxt5SF8gAW65gD2tf+bQJkMaGK4S3RD3W6OLYvdCWrjbhofvhn2ecKkjb
h0ybkG12wpaLOPbbxDgDawj8QGn3KXvBs8UnBV5hYWxVPtjops9L4tzL1kDhaqxH
twIDAQAB
-----END PUBLIC KEY-----
"""


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
        local_machine = get_machine_code()
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
    rsakey = RSA.importKey(PUBLIC_KEY)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    hsmsg = SHA.new()
    hsmsg.update(message_verify)

    is_verify = verifier.verify(hsmsg, b_signature)

    if is_verify is not True:
        raise ValueError("WRONG CODE")
    return content


def check_authfile(filepath):
    """
    Check auth-file
    """
    with open(filepath, 'r') as file_content:
        save = file_content.read()
        if save == '':
            raise ValueError("MISSING CODE")
        return save


def check_license(filepath):
    """
    Execute this app
    """

    if os.path.isfile(filepath) is False:
        raise FileNotFoundError()

    record_code = check_authfile(filepath)
    record_code = decode_rsa(record_code)
    check_key(record_code)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--filepath', type=str, dest="filepath", default='./iam3d.lic')
    args = parser.parse_args()

    try:
        check_license(args.filepath)
        print("OK")
    except Exception as identifier:
        print(identifier)
