import os
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
    data = {}
    if tmp := os.getenv('LOCATION_INFO'):
        data = json.loads(tmp)
    else:
        raise Exception("请在环境变量中设置LOCATION_INFO")
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

    message = '疫情通丨' + message

    server_jiang_push(SCKEY, message)


if __name__ == '__main__':
    main_handler(None, None)
