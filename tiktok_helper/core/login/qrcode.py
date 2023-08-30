import os
import time

import base64
from io import BytesIO

import requests
from PIL import Image

from .. import common

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 '
                  'Safari/537.36 Edg/115.0.1901.203',
    'Referer': 'https://www.douyin.com/',
}


def decode_qrcode(base64_encoded_qrcode):
    # decode
    decoded_qrcode = base64.b64decode(base64_encoded_qrcode)

    # load
    image = Image.open(BytesIO(decoded_qrcode))

    # covert color
    image = image.convert("1")

    return image


def get_qrcode_info():
    get_qrcode_url = 'https://sso.douyin.com/get_qrcode/?service=https%3A%2F%2Flive.douyin.com'

    response = requests.get(get_qrcode_url, headers=headers)
    qrcode_info_json = response.json()

    return qrcode_info_json


def login(qrcode_base64, token):
    # decode and show qrcode
    image = decode_qrcode(qrcode_base64)

    # show img
    image.save("qr_code.png")
    image.show()

    # check qrcode connection url
    check_qrcode_url = 'https://sso.douyin.com/check_qrconnect/?service=https%3A%2F%2Fwww.douyin.com' \
                       + '&token=' + token

    basic_cookie = common.get_basic_cookie()

    # wait user to sacn code
    while True:
        response = requests.get(check_qrcode_url, headers=headers, cookies=basic_cookie)
        qrcode_status_json = response.json()

        # print('=================')
        # print(qrcode_status_json)
        # print('=================')

        # status code: 1 code not scanned; 2 code scanned; 3 success login; 5 timeout;
        status_code = qrcode_status_json['data']['status']
        if status_code == '1':
            print('wait for scanning...')
        elif status_code == '2':
            print('wait for login...')
        elif status_code == '3':
            print('login successfully!')
            # get redirect url
            redirect_url = qrcode_status_json['data']['redirect_url']
            response = requests.get(redirect_url, headers=headers, cookies=basic_cookie, allow_redirects=False)
            # get login cookie
            login_cookie = response.cookies
            # save cookie to local
            common.save_cookie(login_cookie, 'login_cookie')
            return
        else:
            pass
        time.sleep(5)


def qrcode_login():
    # check local cookie
    if os.path.exists(os.path.join('tmp', 'login_cookie')):
        return

    # get qrcode info (json)
    qrcode_info_json = get_qrcode_info()

    # get qrcode in base64 code
    qrcode_base64 = qrcode_info_json['data']['qrcode']

    # get qrcode token
    qrcode_token = qrcode_info_json['data']['token']

    # show qrcode, user scan
    login(qrcode_base64, qrcode_token)