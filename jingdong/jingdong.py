# -*- coding: utf-8 -*-
# File  : jingdong.py
# Author: HuWenBo
# Date  : 2018/11/14
import requests
import time
import json


class JD:
    headers = {
        'referer': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    def __init__(self):
        self.index = 'https://www.jd.com/'
        self.user_url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action?&callback=jsonpUserinfo&_=' + \
                        str(int(time.time() * 1000))  # 检测用户信息
        self.buy_url = 'https://cart.jd.com/gate.action?pid={}&pcount=1&ptype=1'  # 添加到购物车
        self.pay_url = 'https://cart.jd.com/gotoOrder.action'  # 提交订单
        self.pay_success = 'https://trade.jd.com/shopping/order/submitOrder.action'  # 付款页面
        self.goods_id = ''  # 商品id
        self.thor = 'A81BD189F1752D26BDF1CFE6707715876962968B2002F739FAC6FBD81230A94C93D47DDB261C1A7EA481FB4519B254202AC38D06B152CA5D832893BF8E7A810BB91C9D37C3DBC730AEB258623E28D7DAF6BC715DC1715A122D8506CF2983CA73BC0EF9B1AB6B28D9B52881A1EB16180AF039D9B6F25375B9D8FA058B94090BDE7B9AB41CAD5BF5EC0BF7081C581455600D8E3328630A57D3CC49155F6638891A'  # 用户的cookie
        self.rob_url = 'https://itemko.jd.com/itemShowBtn?callback=jQuery972858&skuId={}&from=pc'
        self.session = requests.session()

    def login(self):  # 直接加上cookie访问index是不能看到是否登录成功的,要访问用户信息的url。
        JD.headers['referer'] = 'https://cart.jd.com/cart.action'
        c = requests.cookies.RequestsCookieJar()
        c.set('thor', self.thor)  # 添加用户的thor
        self.session.cookies.update(c)
        response = self.session.get(
            url=self.user_url, headers=JD.headers).text.strip('jsonpUserinfo()\n')
        user_info = json.loads(response)
        print('账号：', user_info.get('nickName'))
        if user_info.get('nickName'):
            self.shopping()
            # self.rob()

    def shopping(self):
        goods_url = input('商品链接：')
        self.goods_id = goods_url[
                        goods_url.rindex('/') + 1:goods_url.rindex('.')]
        JD.headers['referer'] = goods_url
        buy_url = self.buy_url.format(self.goods_id)
        self.session.get(url=buy_url, headers=JD.headers)  # 添加到购物车
        self.session.get(url=self.pay_url, headers=JD.headers)  # 提交订单
        response = self.session.post(
            url=self.pay_success, headers=JD.headers)  # 提交订单
        order_id = json.loads(response.text).get('orderId')

        if order_id:
            print('抢购成功订单号:', order_id)

    def rob(self):
        goods_url = input('商品链接：')
        self.goods_id = goods_url[goods_url.rindex('/') + 1:goods_url.rindex('.')]
        JD.headers['referer'] = goods_url
        rob_url = self.rob_url.format(self.goods_id)  # 抢购前的url
        response = self.session.get(url=rob_url, headers=JD.headers).text.strip('jQuery972858()\n')
        rob_url = 'https:' + json.loads(response).get('url', 'null')  # 抢购url
        response = self.session.get(url=rob_url, headers=JD.headers)
        print(response.text)


if __name__ == '__main__':
    jd = JD()
    jd.login()
