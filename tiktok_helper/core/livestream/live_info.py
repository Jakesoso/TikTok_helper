import requests

from .. import common


def get_info_json(live_id):
    api_url = 'https://live.douyin.com/webcast/room/web/enter/?aid=6383&' \
              'device_platform=&browser_language=&browser_platform=&browser_name=&browser_version=&' \
              f'web_rid={live_id}'

    # get cookie
    cookies = common.get_basic_cookie()

    # Parsing JSON and get like count
    try:
        response = requests.get(api_url, headers=common.headers, verify=False, cookies=cookies)
        live_info_json = response.json()
    except Exception as e:
        print(f"A error occurred when get live json: {str(e)}")
        live_info_json = None
    return live_info_json