import os
import asyncio
import hashlib
from cryptography.fernet import Fernet
import json

from base64 import urlsafe_b64encode as b64e
from base64 import urlsafe_b64decode as b64d

# constants
RB = "rb"
WB = "wb"
R = "r"
W = "w"
AP = "a+"
A = "a"


async def cw_file(path: str, type: str = "r", content: str = ""):
    if os.path.exists(path):
        data = ""
        try:
            with open(path, type) as file:
                if "r" in type:
                    data = file.read()
                    return data
                elif "w" in type:
                    file.write(content)
                    return True
                else:
                    file.close()
                    raise Exception('Type not exists')
                file.close()
        except:
            raise Exception('Some error...')
    else:
        raise Exception('File not found')


async def build(
        container: str,
        parameters: str,
        prefix: str = '[pyColdWallet]',
):
    return b64e("".join(
        [prefix, "/", container, "/", parameters]
    ).encode('utf-8')).decode('utf-8')


async def crypt_container(data: bytes, pass1: bytes, pass2: bytes):
    return Fernet(
        b64e(
            hashlib.md5(
                hashlib.sha3_512(pass1).hexdigest().encode('utf-8')
                +
                hashlib.md5(pass2).hexdigest().encode('utf-8')
            ).hexdigest().encode('utf-8')
        )
    ).encrypt(data)


async def decrypt_container(data: bytes, pass1: bytes, pass2: bytes):
    return Fernet(
        b64e(
            hashlib.md5(
                hashlib.sha3_512(pass1).hexdigest().encode('utf-8')
                +
                hashlib.md5(pass2).hexdigest().encode('utf-8')
            ).hexdigest().encode('utf-8')
        )
    ).decrypt(data)


encoded = asyncio.run(crypt_container(
    data=asyncio.run(cw_file('test.txt', RB)),
    pass1=b'dfnafoaiwhfaowifh',
    pass2=b'faofjoapfwojfwpojo'
))


decoded = asyncio.run(decrypt_container(
    data=encoded,
    pass1=b'dfnafoaiwhfaowifh',
    pass2=b'faofjoapfwojfwpojo'
))

print(decoded)