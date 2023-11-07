from Crypto.Cipher import AES
import base64
from typing import Any


def decrypt_cipher_text(encrypted_data: dict[Any]) -> str:
    iv = base64.b64decode(encrypted_data['iv'])
    key = base64.b64decode(encrypted_data['key'])

    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    password = cipher.decrypt(ciphertext).rstrip(b'\x03').decode('utf-8')  # 解析, 去除填充字符, 并转成 utf-8 编码

    return password


def password_validation(default_account: dict[Any], account: dict[Any]) -> tuple[dict[Any], int]:
    if account["password"] == default_account["password"] and account["username"] == default_account["username"]:
        response = {
            'message': '登入成功',
            'status': 'success',
            'status_code': 200,
        }
    else:
        response = {
            'message': '用户名或密码不正确。',
            'status': 'error',
            'status_code': 401,
        }

    return response, response['status_code']
