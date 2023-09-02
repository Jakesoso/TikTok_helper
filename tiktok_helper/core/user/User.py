# -*- coding: utf-8 -*-
from requests.cookies import RequestsCookieJar

from .. import common
from ..login import qrcode


class User:
    """
    Class of Douyin livestream user.
    For login and other things.
    """

    def __init__(self,
                 live_login_cookie: RequestsCookieJar = None,
                 douyin_login_cookie: RequestsCookieJar = None):

        # login cookie
        self.live_login_cookie = live_login_cookie
        self.douyin_login_cookie = douyin_login_cookie

        # user info
        self.id = None
        self.nickname = None

    def douyin_login(self):
        qrcode.login('douyin')
        self.douyin_login_cookie = common.load_cookie(['douyin_login_cookie'])

    def live_login(self):
        qrcode.login('live.douyin')
        self.live_login_cookie = common.load_cookie(['live_login_cookie'])
