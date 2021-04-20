"""
Generate RSA Key
"""
import base64
from Crypto import Random
from Crypto.PublicKey import RSA
import json
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import SHA




def gen_private_public():
    """
    To generate Private and Public Key
    """

    random_generator = Random.new().read
    # 產生 2048 位元 RSA 金鑰
    key = RSA.generate(2048, random_generator)
    # 保護金鑰的密碼
    secret_code = "secret#code"


    # 以密碼加密保護 RSA 金鑰
    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
                                protection="scryptAndAES128-CBC")

    # 將 RSA 金鑰寫入檔案
    with open("private.pem", "wb") as file_content:
        file_content.write(encrypted_key)
    public_key=key.publickey().exportKey()
    with open("public.pem", "wb") as file_content:
        file_content.write(public_key)

def generate_licensefile(encode):

    data = {'encode':encode}
    with open('licensefile.skm', 'w') as file_content:
        json.dump(data,file_content)

def encode_rsa(content,machine_code):
    """
    To encoded by rsa
    """
    message = machine_code
    file_detail = open("private.pem","rb")
    rsakey = RSA.importKey(file_detail.read(),passphrase='secret#code')
    file_detail.close()
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf-8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    encode = machine_code+"_"+signature.decode('utf-8')+"_"+content
    encode = encode.encode("utf-8")
    encode = base64.b64encode(encode)
    # Decoding the Base64 bytes to string
    encode = encode.decode("UTF-8")
    return encode

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-generatePrivatePublic',\
        help='Generate Private key and Public key',\
        dest="generatePrivatePublic")
    parser.add_argument('-machine_code',help='machine_code',dest="machine_code")
    parser.add_argument('-date', help='Valid date(yyyymmdd)',dest="date")
    parser.add_argument('-reset', help='Generate a pair of new keys',dest="reset")
        #parser.add_argument('-code',help='Input your code',dest="code")
    args = parser.parse_args()
    #date=datetime.datetime.today().strftime("%Y%m%d")

    date="20210421"
    #date = args.date
    #machine_code = args.machine_code
    machine_code="34:c9:3d:47:94:a6"


    gen = input("Generate:(Y/N)")
    #gen=args.generatePrivatePublic
    if args.reset != '':
        gen_private_public()

    code = date
    code+= machine_code
    print("code="+code)
    encode = encode_rsa(code,machine_code)
    generate_licensefile(encode)
    print(encode)
    