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
                    file.close()
                    return data
                elif "w" or "a" in type:
                    file.write(content)
                    file.close()
                    return True
                else:
                    file.close()
                    raise Exception('Type not exists')
        except:
            raise Exception('Some error...')
    else:
        raise Exception('File not found')


async def build(
        container: str,
        parameters: str,
        prefix: str = '[cryptocontainer-py]',
):
    return b64e("".join(
        [prefix, "/", container, "/", parameters]
    ).encode('utf-8')).decode('utf-8')


async def crypt_container(data: bytes, pass1: bytes, pass2: bytes):
    try:
        return Fernet(
            b64e(
                hashlib.md5(
                    hashlib.sha3_512(pass1).hexdigest().encode('utf-8')
                    +
                    hashlib.md5(pass2).hexdigest().encode('utf-8')
                ).hexdigest().encode('utf-8')
            )
        ).encrypt(data)
    except:
        return False


async def decrypt_container(data: bytes, pass1: bytes, pass2: bytes):
    try:
        return Fernet(
            b64e(
                hashlib.md5(
                    hashlib.sha3_512(pass1).hexdigest().encode('utf-8')
                    +
                    hashlib.md5(pass2).hexdigest().encode('utf-8')
                ).hexdigest().encode('utf-8')
            )
        ).decrypt(data)
    except:
        return False


encoded = asyncio.run(crypt_container(
    data=asyncio.run(cw_file('test.txt', RB)),
    pass1=b'dfnafoaiwhfaowifh',
    pass2=b'faofjoapfwojfwpojo'
))


def pack(filename: str, pass1: str, pass2: str):
    encoded = asyncio.run(crypt_container(
        data=asyncio.run(cw_file(filename, RB)),
        pass1=pass1.encode('utf-8'),
        pass2=pass2.encode('utf-8')
    )).decode('utf-8')
    result = asyncio.run(build(
        container=encoded,
        parameters="filename=" + filename
    ))
    return result


def unpack(hash: str, pass1: str, pass2: str):
    data = b64d(hash.encode('utf-8')).decode('utf-8').split('/')
    prefix = data[0]

    # that we should to decode
    container = data[1]

    # that parameters
    params = {}
    for x in data[2].split('+'):
        p_ = x.split('=')
        params[p_[0]] = p_[1]

    asyncio.run(cw_file((params['filename'] if "filename" in list(params) else "output"), WB, content=asyncio.run(decrypt_container(
        data=container.encode('utf-8'),
        pass1=pass1.encode('utf-8'),
        pass2=pass2.encode('utf-8')
    ))))