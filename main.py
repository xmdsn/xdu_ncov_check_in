import requests
import json
import time
import pytz
import datetime


def login(session, username, password):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://xxcapp.xidian.edu.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://xxcapp.xidian.edu.cn/uc/wap/login',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
        'username': username,
        'password': password
    }

    session.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',
                 headers=headers, data=data)


def submit(session):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://xxcapp.xidian.edu.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://xxcapp.xidian.edu.cn/ncov/wap/default/index',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
        'szgjcs': '',
        'szcs': '',
        'szgj': '',
        'zgfxdq': '0',
        'mjry': '0',
        'csmjry': '0',
        'tw': '2',
        'sfcxtz': '0',
        'sfjcbh': '0',
        'sfcxzysx': '0',
        'qksm': '',
        'sfyyjc': '0',
        'jcjgqr': '0',
        'remark': '',
        'address': '陕西省西安市长安区兴隆街道内环北路西安电子科技大学长安校区',
        'geo_api_info': '{"type":"complete","position":{"Q":34.124816351997,"R":108.83649576823001,"lng":108.836496,"lat":34.124816},"location_type":"html5","message":"Get ipLocation failed.Get geolocation success.Convert Success.Get address success.","accuracy":126,"isConverted":true,"status":1,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"264号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道内环北路西安电子科技大学长安校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
        'area': '陕西省 西安市 长安区',
        'province': '陕西省',
        'city': '西安市',
        'sfzx': '1',
        'sfjcwhry': '0',
        'sfjchbry': '0',
        'sfcyglq': '0',
        'gllx': '',
        'glksrq': '',
        'jcbhlx': '',
        'jcbhrq': '',
        'ismoved': '0',
        'bztcyy': '',
        'sftjhb': '0',
        'sftjwh': '0',
        'sfjcjwry': '0',
        'jcjg': ''
    }

    response = session.post('https://xxcapp.xidian.edu.cn/ncov/wap/default/save',
                            headers=headers, data=data)

    s = response.text
    j = json.loads(s)
    return j['m']


def get_hour_message():
    h = datetime.datetime.fromtimestamp(
        int(time.time()), pytz.timezone('Asia/Shanghai')).hour
    if 6 <= h <= 11:
        return '晨'
    elif 12 <= h <= 17:
        return '午'
    elif 18 <= h <= 24:
        return '晚'
    else:
        return '凌晨'


def server_jiang_push(SCKEY: str, message):
    requests.get(f'https://sc.ftqq.com/{SCKEY}.send?text={message}')


def main_handler(event, context):

    student_id = ''
    password = ''  # http://ids.xidian.edu.cn/authserver/login

    # https://sc.ftqq.com/3.version
    # 基于 Server 酱的推送服务,
    SCKEY = ''

    session = requests.session()
    login(session, student_id, password)
    message = submit(session)

    message = get_hour_message() + '检-' + message

    server_jiang_push(SCKEY, message)


if __name__ == '__main__':
    main_handler(None, None)
