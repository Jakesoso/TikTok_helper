import http.cookiejar
import os

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 '
                  'Safari/537.36 Edg/115.0.1901.203',
}


# disable warnings
requests.packages.urllib3.disable_warnings()

# tmp path
tmp_folder_path = 'tmp'


# generate xbogus, mstoken and ttwid
def get_signature(url):
    signature_data = {
        'url': url,
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0'
                     'Safari/537.36 Edg/115.0.1901.203',
    }

    generate_api_url = 'https://tiktok-signature-green.vercel.app/'
    response = requests.post(generate_api_url, json=signature_data)
    return response.json()


# get basic cookies that most request operates need
def get_basic_cookie():
    url_index = 'https://douyin.com'
    url_live_index = 'https://live.douyin.com'
    try:
        cookies = requests.get(url_index, headers=headers, verify=False).cookies
        cookies = requests.get(url_live_index, headers=headers, verify=False, cookies=cookies).cookies
        save_cookie(cookies, 'basic_cookie')
    except Exception as e:
        print(f"A error occurred when get basic cookie:{str(e)}")
        cookies = None
    return cookies


# save cookie to local location
def save_cookie(cookies, filename):
    # create a MozillaCookieJar obj
    cookie_jar = http.cookiejar.MozillaCookieJar()

    # load the cookies into the cookie_jar
    for cookie in cookies:
        cookie_jar.set_cookie(cookie)

    # create tmp folder
    if not os.path.exists(tmp_folder_path):
        os.makedirs(tmp_folder_path)

    # save cookieJar
    file_path = os.path.join(tmp_folder_path, filename)
    try:
        cookie_jar.save(file_path)
        print(f"Cookie saved to {file_path} successfully!")
    except Exception as e:
        print(f"An error occurred when saving {filename} cookie:{str(e)}")


# load cookie from local location
def load_cookie():
    cookie_jar = http.cookiejar.MozillaCookieJar()
    requests_cookie = requests.cookies.RequestsCookieJar()
    try:
        cookie_jar.load(os.path.join(tmp_folder_path, 'basic_cookie'))
        cookie_jar.load(os.path.join(tmp_folder_path, 'login_cookie'))
        for cookie in cookie_jar:
            requests_cookie.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)
        print(f"Cookie loaded from {tmp_folder_path} successfully!")
    except Exception as e:
        print(f"An error occurred when loading cookie: {str(e)}")
    return requests_cookie
