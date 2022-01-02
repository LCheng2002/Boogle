import requests
import json

import sqlite3
from requests.exceptions import RequestException
import numpy as np

import re
import os


def write_to_DB(product_id,user_name, comment):
    # 连接数据库服务 ,如果不存在,会自动生成
    connect = sqlite3.connect('./jingdong_comment.db')
    # 从会话连接生成游标,相当于光标
    cursor = connect.cursor()
    # execute(sql)
    # name Text,      #字符串
    # comment Text      #字符串
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jingdong_comment(
            id INTEGER PRIMARY KEY,
            product_id TEXT,
            name TEXT,     
            comment TEXT     
        );
    """)
    #推荐使用execute方法自带的?占位符，然后传入相同个数的参数。
    cursor.execute("""INSERT INTO jingdong_comment (product_id,name,comment)VALUES (?,?,?);""",[product_id,user_name,comment])

    # 提交确认(插入,更新需要)
    connect.commit()

    cursor.close()
    connect.close()

def parse_one_page(product_id,html):
    comments_dict = json.loads(html) # json.loads()使字符串转换为字典形式
    comment_list = comments_dict["comments"]    # 获取comments标签下的内容，即用户评论信息列表

    for item in comment_list:
        comment = item["content"]
        user_name = item["nickname"]
        write_to_DB(product_id,user_name, comment)


def comment_info(product_id):
    page = "https://club.jd.com/comment/productPageComments.action?callback&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1".format(product_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Referer": "https://item.jd.com/",
        "Cookie": "3AB9D23F7A4B3C9B=VCZP7M7YJRJHRR4NROQDRFF3ONPNOOHFBCEKE7ZIEUEEXC55JZMKKTPWVO4SHCLG5MESPVFRKTQIJP2QSZZLPLYA7A; TrackID=1vNcZZ86gqJVNcn0lA8K4G59CKK2xLMVj00TdQGp_qnK7CJUVAFLcRjOf6c-Tdv-qHTCfTItsNsQ0dPvjX8gFdHIxJKyZMEpjpuUgtmG6ups; shshshfp=3f2984513937efb888928303a78596e4; shshshfpa=1cb72623-1e95-9c4e-2289-c706abc21156-1556477337; shshshsID=862bc6bf080fc3ff757e84c12bd2ac4c_2_1556477358058; shshshfpb=vkqdiZw5URKpR4d1GBRYd6g%3D%3D; __jda=122270672.15564773383761543900726.1556477338.1556477338.1556477338.1; __jdb=122270672.2.15564773383761543900726|1.1556477338; __jdc=122270672; __jdv=122270672|direct|-|none|-|1556477338378; __jdu=15564773383761543900726; areaId=27; ipLoc-djd=27-2376-50230-53671; JSESSIONID=1AA5FC953DBCD87E5B49464911847606.s1",
        "Host": "club.jd.com",
        "DNT": "1",
        "Accept": "*/*",
        "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept - Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.get(page, headers = headers)
    if response.status_code == 200:
        print("获取页面成功！")
        parse_one_page(product_id,response.text)
    else:
        print("获取页面失败，状态码：%d" %response.status_code)

if __name__ == "__main__":
    id_list = np.load("./ID_list_comment.npy")
    try:
        while True:
            print(len(id_list))
            id_ = id_list[0]
            comment_info(id_)
            id_list = id_list[1:]
    except:
        id_list = np.save("ID_list_comment.npy",id_list)
