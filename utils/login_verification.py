import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from typing import Any
from database import user_db


def decrypt_cipher_text(encrypted_data: dict[Any]) -> bytes:
    iv = base64.b64decode(encrypted_data['iv'])
    key = base64.b64decode(encrypted_data['key'])

    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    password = unpad(cipher.decrypt(ciphertext), AES.block_size)  # 解析, 去除填充字符, 并转成 utf-8 编码

    return password


def account_validation(username: str, password: str) -> bool:
    users = user_db.Users

    user_query = users.select().where(
        (users.username == username) & (users.password == password)
    )

    return user_query.exists()

