# -*- coding: utf-8 -*-
import time

import requests
import requests.utils
from selenium import webdriver

from .Goods import Goods
from .LiveStream import LiveStream
from ..user import User


class Cart:
    """
    Class of Douyin livestream cart.
    Some goods info and some useful tools are provided.
    """

    def __init__(self,
                 live_enter_id: str,
                 visit_user: User):
        """
        :param live_enter_id: livestream id
        :param visit_user: user who visit livestream
        """
        # basic instance attribute
        self.live_enter_id = live_enter_id
        self.user = visit_user
        self.info_json = self.get_info_json()

        # cart attribute
        self.name = self.info_json['page_header']['author_shop_info']['name']
        # self.rate = self.info_json['page_header']['author_shop_info']['reputation']['score']
        self.rate = 0

        # goods attribute
        self.goods_list = self.get_goods_list()

    def get_info_json(self):
        # check login status
        print('===checking login status===')
        if self.user.live_login_cookie is None:
            # not login yet, let user login
            self.user.live_login()

        # create a Selenium WebDriver
        driver = webdriver.ChromiumEdge()
        driver.get('https://live.douyin.com')

        # set login cookie for WebDriver
        for name, value in self.user.live_login_cookie.items():
            driver.add_cookie({'name': name, 'value': value})

        # visit livestream
        print('===visit livestream===')
        live_url = f'https://live.douyin.com/{self.live_enter_id}'
        driver.get(live_url)

        # visit cart by click
        print('===visit yellow cart===')
        cart_element = driver.find_element('xpath', '//div[@data-e2e="yellowCart-container"]/div/span')
        driver.execute_script('arguments[0].click()', cart_element)

        # wait for captcha verify (until 'buy' button show up)
        while not driver.find_elements('xpath', '//button[@data-e2e="shop-buyBtn"]'):
            print('请手动完成抖音直播间的验证!')
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
        livestream = LiveStream(self.live_enter_id)
        api_url = 'https://live.douyin.com/live/promotions/page/?aid=6383' \
                  f'&room_id={livestream.room_id}&author_id={livestream.streamer_id}' \
                  f'&offset=0&limit=100'  # offset: begin position; limit: count; max limit is 100
        return session.get(api_url).json()

    def get_goods_list(self):
        """
        Get goods list from JSON.
        :rtype: list
        """
        goods_list = []
        for pre_json in self.info_json['promotions']:
            # generate dict
            try:
                campaign_info = pre_json['campaign_info']
                stock = campaign_info['left_stock']
                price = campaign_info['price']
                goods_id = campaign_info['campaign_id']
            except KeyError:    # some goods may not have 'campaign_info'
                stock = ''
                price = 0.00
                goods_id = ''
            goods_dict = {'stock': stock,
                          'description': pre_json['elastic_title'],
                          'name': pre_json['title'],
                          'price': price,
                          'id': goods_id,}
            goods_list.append(Goods(goods_dict))
        return goods_list

    def __str__(self):
        # transform all goods info into str
        goods_str = [f"[{i+1}]\n{str(good)}" for i, good in enumerate(self.goods_list)]
        goods_str = '\n'.join(goods_str)

        return "===直播间带货信息===\n" \
               f"房间进入号码: {self.live_enter_id}\n" \
               f"店铺名: {self.name}\n" \
               f"店铺评分: {self.rate}\n" \
               f"==商品信息==\n{goods_str}\n"
