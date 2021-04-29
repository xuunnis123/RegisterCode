"""
Generate RSA Key
"""
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import SHA


def generate_licensefile(encode):
    with open('licensefile.skm', 'w') as file_content:
        file_content.write(encode)


def encode_rsa(content):
    """
    To encode with rsa
    """
    message = content.upper().replace(":", "")

    with open("private.pem", "rb") as file_detail:
        file_detail_content = file_detail.read()

    rsakey = RSA.importKey(file_detail_content, passphrase='secret#code')

    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf-8"))
    sign = signer.sign(digest)

    message = message.encode("utf-8")
    encode = message+b'_'+sign
    encode = base64.b64encode(encode)
    encode = encode.decode("UTF-8")
    return encode


if __name__ == '__main__':

    date = "20210429"
    machine_code = "34:c9:3d:47:94:a6"

    code = date + "_"
    code += machine_code

    encode = encode_rsa(code)
    generate_licensefile(encode)
    print(encode)
