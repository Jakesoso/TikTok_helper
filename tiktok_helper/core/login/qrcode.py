import base64
import time
from io import BytesIO

import requests
from PIL import Image
from requests import Response
from requests.cookies import RequestsCookieJar

from .. import common

headers = common.headers.copy().update({'Referer': 'https://www.douyin.com/'})


def decode_qrcode(base64_encoded_qrcode) -> Image:
    # decode
    decoded_qrcode = base64.b64decode(base64_encoded_qrcode)

    # load
    image = Image.open(BytesIO(decoded_qrcode))

    # covert color
    image = image.convert("1")

    return image


def get_qrcode_info() -> Response.json:
    get_qrcode_url = 'https://sso.douyin.com/get_qrcode/?service=https%3A%2F%2Flive.douyin.com'

    response = requests.get(get_qrcode_url, headers=headers)
    qrcode_info_json = response.json()

    return qrcode_info_json


def show_and_scan(platform: str, qrcode_base64, token: str) -> RequestsCookieJar:
    # decode and show qrcode
    image = decode_qrcode(qrcode_base64)

    # show img
    image.save("qr_code.png")
    image.show()

    # check qrcode connection url
    pre_url = 'douyin' if platform == 'douyin' else 'live.douyin'
    check_qrcode_url = 'https://sso.douyin.com/check_qrconnect/?service=https%3A%2F%2F' \
                       f'www.{pre_url}.com&token={token}'

    basic_cookie = common.get_basic_cookie()

    # wait user to sacn code
    while True:
        session = requests.session()
        response = session.get(check_qrcode_url, headers=headers, cookies=basic_cookie)
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
            session.get(redirect_url, headers=headers)
            # get login cookie
            login_cookie = session.cookies
            # save cookie to local
            cookie_name = 'douyin_login_cookie' if platform == 'douyin' else 'live_login_cookie'
            common.save_cookie(login_cookie, cookie_name)
            return login_cookie
        else:
            pass
        time.sleep(5)


def login(platform: str) -> None:
    # check local cookie
    cookie_name = 'douyin_login_cookie' if platform == 'douyin' else 'live_login_cookie'
    if common.load_cookie([cookie_name]) is not None:
        return

    print('===logining===')

    # get qrcode info (json)
    qrcode_info_json = get_qrcode_info()

    # get qrcode in base64 code
    qrcode_base64 = qrcode_info_json['data']['qrcode']

    # get qrcode token
    qrcode_token = qrcode_info_json['data']['token']

    # show qrcode, user scan
    show_and_scan(platform, qrcode_base64, qrcode_token)
