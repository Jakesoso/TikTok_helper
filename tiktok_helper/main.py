from core.livestream import live_info
from core.login import qrcode

'''
    this is an example usage.
'''

if __name__ == '__main__':
    # login method
    qrcode.login('douyin')

    # get livestream like count
    live_id = '336586944484'
    like_count = live_info.get_like_count(live_id)
    print(like_count)