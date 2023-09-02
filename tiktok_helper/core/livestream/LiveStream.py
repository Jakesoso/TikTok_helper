# -*- coding: utf-8 -*-
import requests
from requests.cookies import RequestsCookieJar

from .. import common


class LiveStream:
    """
    Class of Douyin livestream.
    Some livestream info and some useful tools are provided.
    """

    def __init__(self,
                 live_enter_id: str,
                 visit_cookie: RequestsCookieJar = common.get_basic_cookie()):
        """
         :param live_enter_id: livestream id
         :param visit_cookie: cookie which is loaded to visit livestream
         """
        # basic attribute
        self.enter_id = live_enter_id
        self.cookie = visit_cookie
        self.header = common.headers
        self.api_url = 'https://live.douyin.com/webcast/room/web/enter/?aid=6383&' \
                       'device_platform=&browser_language=&browser_platform=&' \
                       f'browser_name=&browser_version=&web_rid={self.enter_id}'
        self.info_json = self.get_info_json()['data']['data'][0]

        # livestream attribute
        self.room_id = self.info_json['id_str']
        self.title = self.info_json['title']
        self.audience_count = self.info_json['user_count_str']
        self.likes_count = self.info_json['like_count']
        # streamer attribute
        self.streamer_name = self.info_json['owner']['nickname']
        self.streamer_id = self.info_json['owner']['id_str']
        # cart attribute
        self.cart_quantity = self.info_json['room_cart']['total']

    def get_info_json(self):
        """
         Get the basic livestream info in JSON.
         """
        # Parsing JSON and get like count
        try:
            response = requests.get(self.api_url,
                                    headers=self.header,
                                    cookies=self.cookie)
            return response.json()
        except Exception as e:
            print(f"A error occurred when get live json: {str(e)}")
            return None

    def __str__(self):
        """
        Show livestream info in a more clear way
        """
        return "===直播间信息===\n" \
               f"房间进入号码: {self.enter_id}\n" \
               f"房间号: {self.room_id}\n" \
               f"标题: {self.title}\n" \
               f"观众人数: {self.audience_count}\n" \
               f"主播: {self.streamer_name}\n" \
               f"点赞数: {self.likes_count}\n" \
               f"购物车数量: {self.cart_quantity}"
