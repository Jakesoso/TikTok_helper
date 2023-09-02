from core.livestream.Cart import Cart
from core.livestream.LiveStream import LiveStream
from core.user.User import User

'''
    this is an usage example.
'''

if __name__ == '__main__':
    # login (not recommend)
    # qrcode.login('douyin')
    # qrcode.login('live.douyin')

    # user login (recommend) [args optional]
    user = User()

    # get livestream info
    live_id = '336586944484'
    live = LiveStream(live_id)
    print(live)

    # get livestream cart info
    cart = Cart(live_id, user)
    print(cart)
    print(cart.get_pop_goods())
