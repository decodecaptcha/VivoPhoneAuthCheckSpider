# -*- coding: utf-8 -*-
# @Author : 艾登科技
# @Email : aidencaptcha@gmail.com
# @Address : https://github.com/aidencaptcha

# # VivoPhoneAuthCheckSpider

# DingxiangCaptchaBreak 【vivo官网-手机真伪查询】 案例

# api 地址

# * [DingxiangCaptchaBreak](https://github.com/aidencaptcha/DingxiangCaptchaBreak)

# 有需求请在邮箱联系

# aidencaptcha@gmail.com


# TODO: 名词解释/字段说明
# ak
# 验证公钥。32位字符串, 验证码的唯一标识, 对公众可见, 用以区分不同页面的验证模块。ID在顶象后台创建获得, 请在每个验证场景部署不同的验证ID。
# 这里以《VIVO官网--IMEI码查询》为案例 https://www.vivo.com.cn/service/mobilePhoneAuthenticityCheck/query
# ak = "1c66b18c06a34d96475e104344d8d9e2", # VIVO官网

# token
# 付费用户获取艾登科技的授权token
#  "token": "************"

# proxy
# 代理格式说明:
# "http://ip:port", # http代理, 无密码
# "http://user:pass@ip:port", # http代理, 有密码
# "http://www.xxx.com:port", # 隧道代理
# "socks5://user:pass@ip:port" # socks代理, 有密码
# 总结: 只要是 requests, scrapy 请求库支持的代理格式都可以
# proxy = "http://127.0.0.1:8888"


import json
import random
import time
from urllib.parse import urlencode
import requests
from parsel import Selector
from loguru import logger
# from huxiu_encrypt import username_encrypt

# 安装 python 第三方依赖
# pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/


logger.debug(r"""
    _     _      _                ____                _          _
   / \   (_)  __| |  ___  _ __   / ___|  __ _  _ __  | |_   ___ | |__    __ _ 
  / _ \  | | / _` | / _ \| '_ \ | |     / _` || '_ \ | __| / __|| '_ \  / _` |
 / ___ \ | || (_| ||  __/| | | || |___ | (_| || |_) || |_ | (__ | | | || (_| |
/_/   \_\|_| \__,_| \___||_| |_| \____| \__,_|| .__/  \__| \___||_| |_| \__,_|
                                              |_|
@Author : 艾登科技
@Email : aidencaptcha@gmail.com
@Address : https://github.com/aidencaptcha
@Description : API需求请在邮箱联系 aidencaptcha@gmail.com
""")


def vivo(ak, proxy, token, imei):
    """ DingxiangCaptchaBreak 【vivo官网-手机真伪查询】 案例 """
    # 请求1, 请求 艾登科技API
    api_url = "http://x.x.x.x:8003/dxcap_api"
    headers = {
        "Connection": "close",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "ak": ak,
        "proxy": proxy,
        "token": token
    })
    response = requests.request("POST", api_url, data=data, headers=headers, timeout=30)
    assert response.text, "response.text is empty"
    res_json = json.loads(response.text)
    # logger.debug(res_json)

    # 解析 艾登科技API 响应
    if res_json["succ"] == 1:
        # result 如果是空字符串"", 代表是推入消费队列操作
        if res_json["result"] == "":
            logger.debug(f'任务已推入消费队列, 等待被消费, 当前任务数: {res_json["count"]}, 当前队列积压数: {res_json["reply"]-1}')
            return

        err_msg = res_json["result"]["err_msg"]
        # err_msg 不等于空字符串，统一当异常忽略
        if err_msg != "":
            return

        # 提取令牌
        data = res_json["result"]["data"]
        logger.debug(f"dx 令牌: {data}")

        ticket = data
        # 请求 2 -- 前端业务请求
        # 根据获取到的令牌, 进行前端业务请求
        vivo_url = "https://www.vivo.com.cn/service/mobilePhoneAuthenticityCheck/query"
        payload = f'imei={imei}&ticket={ticket}%3A6548aa22tSoM0H0N2eeOCf9F65QJNwRWO0dmzZo1&constID=CID%3A{int(time.time()*1000)}'
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://www.vivo.com.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.vivo.com.cn/service/mobilePhoneAuthenticityCheck/index',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
            'Cookie': 'webp_showjoy=available; cookieId=16bf4f32-5383-2e7a-7451-84dc3c5aa8ad1698474735322; _dx_uzZo5y=efea44d78efdf0a474dbe2912ccad8a332794ab1c5eca404b0ea739b81ac300e0c7f48b4; sessionId=19ced20f-c4fe-5091-49fa-372d83f9b83e; pageTAG=0; Hm_lvt_9ef7debb81babe8b94af7f2c274869fd=1698474736,1699222545; Hm_lpvt_9ef7debb81babe8b94af7f2c274869fd=1699222545; JSESSIONID=1522FE92E524E542C89F021834488879; is_vivo=false; Hm_lvt_010739a46d3290bbc78e3b23bfd7b5af=1698474786,1699259718; Hm_lpvt_010739a46d3290bbc78e3b23bfd7b5af=1699259895; _dx_app_1c66b18c06a34d96475e104344d8d9e2=6548a5fc83goigG5xUV7aiTq5ueVqcbhuQ5SoII1; _dx_captcha_vid=18BA3C87A1E1C66B18C067B3CA8A8986A448A9F43F296CCDFB8D3; JSESSIONID=533E710738071E1E6FE78356E6030857'
        }

        response = requests.request("POST", vivo_url, headers=headers, data=payload, proxies={"all": proxy})
        # logger.debug(response.text)

        # 解析html响应
        sel = Selector(response.text)
        content = sel.xpath('//main[@class="content"]')
        title = content.xpath('./h2/text()').get().strip()
        info_content = content.xpath('./div[2]/div[1]/div/div[2]/div//text()').getall()
        info_content = [x for x in info_content if x!='\n']

        # logger.debug(title + ": "+ str(info_content))
        return title + ": "+ str(info_content), ticket

    else:
        logger.debug("请求失败, 请联系技术")
        return


if __name__ == '__main__':
    # 顶象为每个验证场景部署的唯一appkey
    ak = "1c66b18c06a34d96475e104344d8d9e2"
    # 付费用户获取艾登科技的授权token
    token = "******"
    # 使用的代理
    # proxy = "http://127.0.0.1:7890"
    # 虚拟的 IMEI 列表
    imei_list = ['866723019683291', '867683028304892', '867683028304884']

    # 启动
    count = 0
    for i in range(10):
        # proxy = random.choice(["", "http://127.0.0.1:7890"])
        # proxy = ""
        proxy = "http://127.0.0.1:7890"
        imei = random.choice(imei_list)
        res = vivo(ak, proxy, token, imei)
        if res:
            text, ticket = res
            logger.debug(f"【vivo官网-手机真伪查询】 IMEI: {imei}, 顶象令牌：{ticket}, 查询响应: {text}, 查询次数: {count+1}")
            count += 1
        else:
            pass

        # 速度限制
        time.sleep(1)