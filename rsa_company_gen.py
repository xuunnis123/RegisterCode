"""
Generate RSA Key
"""
import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import SHA

from machine_code import get_machine_code


def generate_licensefile(encode, output):
    with open(output, 'w') as file_content:
        file_content.write(encode)


def encode_rsa(content):
    """
    To encode with rsa
    """
    message = content

    with open(os.path.join(os.path.dirname(__file__), "private.pem"), "rb") as file_detail:
        file_detail_content = file_detail.read()

    rsakey = RSA.importKey(file_detail_content, passphrase='9dcr69wPk7Tu2pzTYAUWk4Rw9PBCqUn2')

    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf-8"))
    sign = signer.sign(digest)

    message = message.encode("utf-8")
    encode = message + b'_' + sign
    encode = base64.b64encode(encode)
    encode = encode.decode("UTF-8")
    return encode


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--machine-code', type=str, dest="machine_code", default=get_machine_code())
    parser.add_argument('--date', help='Valid date(yyyymmdd)', type=str, dest="date", required=True)
    parser.add_argument('--output', type=str, dest="output", default='iam3d.lic')
    args = parser.parse_args()

    date = args.date

    code = date + "_"
    code += args.machine_code

    encode = encode_rsa(code)
    generate_licensefile(encode, args.output)
    print(encode)
