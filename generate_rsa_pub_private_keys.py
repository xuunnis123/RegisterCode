from Crypto import Random
from Crypto.PublicKey import RSA

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
    
    with open("public.pem", "wb") as file_content:
        file_content.write(public_key)

if __name__ == '__main__':
    gen_private_public()