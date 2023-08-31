import time

import requests
import requests.utils
from selenium import webdriver

from .live_info import get_info_json
from .. import common
from ..login import qrcode


def get_goods_list(live_id):
    # login and get cookie
    print('======login======')
    qrcode.login('live.douyin')
    cookies = common.load_cookie(['live_login_cookie', 'basic_cookie'])

    # create a Selenium WebDriver
    driver = webdriver.ChromiumEdge()
    driver.get('https://live.douyin.com')

    # set login cookie for WebDriver
    for name, value in cookies.items():
        driver.add_cookie({'name': name, 'value': value})

    # check login status
    driver.get('https://live.douyin.com')

    print('======visit livestream======')

    # visit livestream
    live_url = f'https://live.douyin.com/{live_id}'
    driver.get(live_url)

    print('======visit yellow cart======')

    # visit cart by click
    cart_element = driver.find_element('xpath', '//div[@data-e2e="yellowCart-container"]/div/span')
    driver.execute_script('arguments[0].click()', cart_element)

    # wait for captcha verify (until 'buy' button show up)
    while not driver.find_elements('xpath', '//button[@data-e2e="shop-buyBtn"]'):
        print('Please complete the TikTok verification manually!')
        time.sleep(3)

    # save cookie
    driver_cookies = driver.get_cookies()

    # close driver
    driver.quit()

    # get cookie back to session
    session = requests.Session()
    for cookie in driver_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # re-visit cart by url
    live_info_json = get_info_json(live_id)
    room_id = live_info_json['data']['data'][0]['id_str']
    author_id = live_info_json['data']['data'][0]['owner']['id_str']
    # offset: begin position; limit: count; max limit is 100
    api_url = 'https://live.douyin.com/live/promotions/page/?aid=6383' \
              f'&room_id={room_id}&author_id={author_id}&offset=0&limit=100'

    # get goods info
    goods_json_info = session.get(api_url).json()

    # repack list
    goods_list = []
    for goods in goods_json_info['promotions']:
        goods_list.append(goods)

    return goods_list
