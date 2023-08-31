from core.livestream import live_info
from core.livestream import goods_info
from core.login import qrcode

'''
    this is an example usage.
'''

if __name__ == '__main__':
    # login method
    qrcode.login('douyin')
    # qrcode.login('live.douyin')

    # get livestream like count
    live_id = '336586944484'
    like_count = live_info.get_like_count(live_id)
    print(like_count)

    # get goods list
    goods_list = goods_info.get_goods_list(live_id)

    # print names in goods list for example
    print('======goods list======')
    cnt = 1
    for goods in goods_list:
        goods_name = goods.get('title')
        print(f'No{cnt}: {goods_name}')
        cnt += 1
