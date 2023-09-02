# -*- coding: utf-8 -*-

class Goods:
    """
    Class of Douyin goods in livestream cart.
    Some goods info and some useful tools are provided.
    """

    def __init__(self, info: dict):
        self.stock = info.get('stock')
        self.description = info.get('description')
        self.name = info.get('name')
        self.price = info.get('price') / 100
        self.id = info.get('id')

    def __str__(self):
        return f"商品号: {self.id}\n" \
               f"名称: {self.name}\n" \
               f"介绍: {self.description}\n" \
               f"价格: {self.price if self.price != 0 else ''}\n"
