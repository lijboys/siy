# coding:utf-8


"""
注意事项：
1、邀请源码仅供小伙伴们交流学习，严禁用于牟取任何不正当利益。
2、代码底层架构较老，可以对程序进行二改升级。
3、二改的代码外部分享时必须标注原架构开发者【B站-纸鸢花的花语】。
4、以上事项违反或无视者均无权使用或二改邀请源码。

程序开发者升级建议：
    1、增强个人身份信息随机性，可对请求中的UA、ua、email、iPhoneModel里的参数编写随机函数。
    2、增强客户端信息随机性，可对请求中的客户端version[本程序中为固定值1.38.0]、加密的Salts值[每个版本都有不同Salts]进行随机化。
    3、增强IP信息随机性，可对请求时的IP信息进行代理，使用特殊方法使请求时的IP地址随机化。
    4、增强人为操作真实性，尽量模拟人为操作中的请求方法，本程序只对关键请求进行模拟，未做模拟人为操作的过度修饰。
    5、纸鸢小屋Q群【801730999[技术群有验证]、891085087、187860349】，十分欢迎技术大佬加入技术群，研究各种黑科技技术；其他小伙伴也可在闲聊群中吃瓜趣事。
个人修改：
    1、增加多个临时邮箱后缀以及6个随机邮箱接口，自主选择，其中 1 号邮箱不在随机选择里，因为经常出问题但是又保留着
    2、脚本修改作者GitHub：https://github.com/LiJunYi2
    3、脚本基于Atong管理员基础上进行修改。
    4、重新配置多个随机设备以及多个版本的Salts值，感谢作者【纸鸢花的花语】的视频教程。
    5、接入的随机邮箱：temp-mail.io、tempmail.plus、mail.cx/td、mail.tm/gw
    6、下载 Python 编辑器，安装requests模块再运行即可，苹果用户建议 AppStore 搜索 Python Editor APP直接运行。
    实在不会的，直接丢到 https://replit.com/ 里面去运行。
"""

import requests
import json
import uuid
import hashlib
import time
import random
import string
import re


# ==============验证码加密函数=============


def r(e, t):
    n = t - 1
    if n < 0:
        n = 0
    r = e[n]
    u = r['row'] // 2 + 1
    c = r['column'] // 2 + 1
    f = r['matrix'][u][c]
    l = t + 1
    if l >= len(e):
        l = t
    d = e[l]
    p = l % d['row']
    h = l % d['column']
    g = d['matrix'][p][h]
    y = e[t]
    m = 3 % y['row']
    v = 7 % y['column']
    w = y['matrix'][m][v]
    b = i(f) + o(w)
    x = i(w) - o(f)
    return [s(a(i(f), o(f))), s(a(i(g), o(g))), s(a(i(w), o(w))), s(a(b, x))]


def i(e):
    return int(e.split(",")[0])


def o(e):
    return int(e.split(",")[1])


def a(e, t):
    return str(e) + "^⁣^" + str(t)


def s(e):
    t = 0
    n = len(e)
    for r in range(n):
        t = u(31 * t + ord(e[r]))
    return t


def u(e):
    t = -2147483648
    n = 2147483647
    if e > n:
        return t + (e - n) % (n - t + 1) - 1
    if e < t:
        return n - (t - e) % (n - t + 1) + 1
    return e


def c(e, t):
    return s(e + "⁣" + str(t))


def img_secret(e, t, n):
    return {
        'ca': r(e, t),
        'f': c(n, t)
    }


def item_compare(img_list, mode_list):
    score = 0
    rank = 0
    for i in range(3):
        for j in range(3):
            if img_list[i][j] != mode_list[i][j]:
                score += 1
    # print(core)
    if score == 2:
        rank += 1
    return rank


def list_compare(frames):
    score_list = []
    flag = 0
    for frame in frames:
        img_list = frame["matrix"]
        scores = 0
        for mode_frame in frames:
            mode_list = mode_frame["matrix"]
            one_score = item_compare(img_list, mode_list)
            scores += one_score
        score_list.append(scores)
        flag += 1
    # print(score_list)
    for i in range(12):
        if score_list[i] == 11:
            print("Currently verify the correct serial number of the image：", i)
            return i


def get_random_number(n):
    return random.randint(0, n - 1)


# ============请求参数信息预处理============


# 设置请求头基本信息
basicRequestHeaders_1 = {
    "Accept-Language": "zh",
    "Content-Type": "application/json; charset=utf-8",
    "Host": "user.mypikpak.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "content-type": "application/json"
}

basicRequestHeaders_2 = {
    "x-requested-with": "com.pikcloud.pikpak",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie": "mainHost=user.mypikpak.com"
}

# 获取 salts 以及 UA 常量值
salts_list = [
    {
        "v": "1.38.0",
        "algorithms": [{"alg": "md5", "salt": "Z1GUH9FPdd2uR48"},
                       {"alg": "md5", "salt": "W4At8CN00YeICfrhKye"},
                       {"alg": "md5", "salt": "WbsJsexMTIj+qjuVNkTZUJxqUkdf"},
                       {"alg": "md5", "salt": "O56bcWMoHaTXey5QnzKXDUETeaVSD"},
                       {"alg": "md5", "salt": "nAN3jBriy8/PXGAdsn3yPMU"},
                       {"alg": "md5", "salt": "+OQEioNECNf9UdRe"},
                       {"alg": "md5", "salt": "2BTBxZ3IbPnkrrfd/"},
                       {"alg": "md5", "salt": "gBip5AYtm53"},
                       {"alg": "md5", "salt": "9FMyrvjZFZJT5Y+b1NeSYfs5"},
                       {"alg": "md5", "salt": "0cIBtEVWYCKdIOlOXnTJPhLGU/y5"},
                       {"alg": "md5", "salt": "92j4I+ZiMyxFx6Q"},
                       {"alg": "md5", "salt": "xNFN9RnUlu218s"},
                       {"alg": "md5", "salt": "UZcnnQ2nkaY0S"}]
    },
    {
        "v": "1.39.0",
        "algorithms": [{"alg": "md5", "salt": "e1d0IwHdz+CJLzskoFto8SSKobPWMwcz"},
                       {"alg": "md5", "salt": "wUU7Rz/wpuHy"},
                       {"alg": "md5", "salt": "dye78dKP7wgEFMebN/Z11VVPAAtueAVR3TcMFZPCO0F9mBQqbk/qpHy9Yqr0no"},
                       {"alg": "md5", "salt": "Cpx1E/O+bo+vTguIiLosm3zR9Y1N"},
                       {"alg": "md5", "salt": "uqyFMWT5R6TxXji2DhHxlNYY3"},
                       {"alg": "md5", "salt": "7afNTr/GwzoNJCLXJVm+nEMBa2w8PiwBfm"},
                       {"alg": "md5", "salt": "glbIrXW34T5ceIBUhsAOzT1R0XSHnTwv1mqtg1r"},
                       {"alg": "md5", "salt": "l"},
                       {"alg": "md5", "salt": "51sgGDapT73pQMI664"}]
    },
    {
        "v": "1.40.0",
        "algorithms": [{"alg": "md5", "salt": "MNn/o2kDbAdap6iyA62c31+odfAXm"},
                       {"alg": "md5", "salt": "GU2DNPxJQz8Zd/HZhKe+Vpr3nydASi"},
                       {"alg": "md5", "salt": "Mr"},
                       {"alg": "md5", "salt": "9yuMfCUj3370cqowx0iLT4WI"},
                       {"alg": "md5", "salt": "sEtFM"},
                       {"alg": "md5", "salt": "57O4iXpaXLGJ5CuIXlKWm"},
                       {"alg": "md5", "salt": "jIPlqvJR/1fNI3v4IvFcRv2IlzSuUc"},
                       {"alg": "md5", "salt": "p0u2aV"},
                       {"alg": "md5", "salt": "AnHbAEWs+4ggDbg37bbpULXK2NFyFHSE"},
                       {"alg": "md5", "salt": "X3v/UHqblw2VHjeCJHamvXyB"},
                       {"alg": "md5", "salt": "Lxe9yYKLa7JBTw3AKivrzs+CqdGO39K"},
                       {"alg": "md5", "salt": "lkz8Q4viV1+U"},
                       {"alg": "md5", "salt": "VH2I"}]
    },
    {
        "v": "1.41.0",
        "algorithms": [{"alg": "md5", "salt": "Wcpe+bWhLidcpKx+NbicS9tmSq8RbVTFk6Arf"},
                       {"alg": "md5", "salt": "/WcDjchZab"},
                       {"alg": "md5", "salt": "YWRJGUPI/lD"},
                       {"alg": "md5", "salt": "R"},
                       {"alg": "md5", "salt": "9Kba0Nkh7vz5CGWxgFCyqJ/BdjnJIx8KU5r/WTR6Ae"},
                       {"alg": "md5", "salt": "tmUQGnovPWmNvB0UAQbDZnJMg57jGzUv7"},
                       {"alg": "md5", "salt": "sPsOQdEqCp19PUDMYfg1//"},
                       {"alg": "md5", "salt": "mvhuvTJROSortMaGzK5rZi209sBTZq+WitI"},
                       {"alg": "md5", "salt": "Qox5BNaQfdishhmAKGr"},
                       {"alg": "md5", "salt": "R2JW9N8bRUEizf+pkWg/o9iJKG34bdpSjEe"},
                       {"alg": "md5", "salt": "FvDT"}]
    },
    {
        "v": "1.42.6",
        "algorithms": [{"alg": "md5", "salt": "frupTFdxwcJ5mcL3R8"},
                       {"alg": "md5", "salt": "jB496fSFfbWLhWyqV"},
                       {"alg": "md5", "salt": "xYLtzn8LT5h3KbAalCjc/Wf"},
                       {"alg": "md5", "salt": "PSHSbm1SlxbvkwNk4mZrJhBZ1vsHCtEdm3tsRiy1IPUnqi1FNB5a2F"},
                       {"alg": "md5", "salt": "SX/WvPCRzgkLIp99gDnLaCs0jGn2+urx7vz/"},
                       {"alg": "md5", "salt": "OGdm+dgLk5EpK4O1nDB+Z4l"},
                       {"alg": "md5", "salt": "nwtOQpz2xFLIE3EmrDwMKe/Vlw2ubhRcnS2R23bwx9wMh+C3Sg"},
                       {"alg": "md5", "salt": "FI/9X9jbnTLa61RHprndT0GkVs18Chd"}]
    }
]

ua_list = [
    {
        "name": "华为/荣耀（旧）",
        "value": "HUAWEI",
        "models": [
            {"name": "HUAWEI Mate X3", "value": "ALT-AL00"},
            {"name": "HUAWEI Mate X2 典藏版", "value": "TET-AN50"},
            {"name": "HUAWEI Mate X2", "value": "TET-AN00"},
            {"name": "HUAWEI Mate X", "value": "TAH-AN00"},
            {"name": "HUAWEI Mate Xs 2 典藏版", "value": "PAL-AL00-DC"},
            {"name": "HUAWEI Mate Xs 2", "value": "PAL-AL00"},
            {"name": "HUAWEI Mate Xs", "value": "TAH-AN00m"},
            {"name": "HUAWEI Mate 50 RS", "value": "DCO-AL00-PD"},
            {"name": "HUAWEI Mate 50 Pro", "value": "DCO-AL00"},
            {"name": "HUAWEI Mate 50", "value": "CET-AL00"},
            {"name": "HUAWEI Mate 50E", "value": "CET-AL60"},
            {"name": "HUAWEI Mate 40 RS", "value": "NOP-AN00-PD"},
            {"name": "HUAWEI Mate 40 Pro+", "value": "NOP-AN00"},
            {"name": "HUAWEI Mate 40 Pro", "value": "NOH-AN00"},
            {"name": "HUAWEI Mate 40", "value": "OCE-AN10"},
            {"name": "HUAWEI Mate 40E", "value": "OCE-AN50"},
            {"name": "HUAWEI Mate 30 RS", "value": "LIO-AN00P"},
            {"name": "HUAWEI Mate 30 Pro 5G", "value": "LIO-AN00"},
            {"name": "HUAWEI Mate 30 5G", "value": "TAS-AN00"},
            {"name": "HUAWEI Mate 30 Pro", "value": "LIO-AL00"},
            {"name": "HUAWEI Mate 30", "value": "TAS-AL00"},
            {"name": "HUAWEI Mate 30E Pro 5G", "value": "LIO-AN00m"},
            {"name": "HUAWEI P60 Pro", "value": "MNA-AL00"},
            {"name": "HUAWEI P60", "value": "LNA-AL00"},
            {"name": "HUAWEI P50 Pocket", "value": "BLA-AL80"},
            {"name": "HUAWEI P50 Pro", "value": "JAD-AL80"},
            {"name": "HUAWEI P50", "value": "ABR-AL80"},
            {"name": "HUAWEI P50E", "value": "ABR-AL90"},
            {"name": "HUAWEI P40 Pro+", "value": "ELS-AN10"},
            {"name": "HUAWEI P40 Pro", "value": "ELS-AN00"},
            {"name": "HUAWEI P40", "value": "ANA-AN00"},
            {"name": "HUAWEI P40 4G", "value": "ANA-AL00"},
            {"name": "HUAWEI P30 Pro", "value": "VOG-AL10"},
            {"name": "HUAWEI P30", "value": "ELE-AL00"},
            {"name": "HUAWEI Pocket S", "value": "BAL-AL60"},
            {"name": "HUAWEI nova 11 Ultra", "value": "GOA-AL80U"},
            {"name": "HUAWEI nova 11 Pro", "value": "GOA-AL80"},
            {"name": "HUAWEI nova 11", "value": "FOA-AL00"},
            {"name": "HUAWEI nova 10 Pro", "value": "GLA-AL00"},
            {"name": "HUAWEI nova 10", "value": "NCO-AL00"},
            {"name": "HUAWEI nova 10 SE", "value": "BNE-AL00"},
            {"name": "HUAWEI nova 10z", "value": "CHA-AL80"},
            {"name": "HUAWEI nova 10青春版", "value": "JLN-AL00"},
            {"name": "HUAWEI nova 9 Pro", "value": "RTE-AL00"},
            {"name": "HUAWEI nova 9", "value": "NAM-AL00"},
            {"name": "HUAWEI nova 9 SE", "value": "JLN-AL00"},
            {"name": "荣耀30S", "value": "CDY-AN90"},
            {"name": "荣耀30 Pro+", "value": "EBG-AN10"},
            {"name": "荣耀30 Pro", "value": "EBG-AN00"},
            {"name": "荣耀30", "value": "BMH-AN10"},
            {"name": "荣耀30 青春版", "value": "MXW-AN00"},
            {"name": "荣耀V30 Pro", "value": "OXF-AN10"},
            {"name": "荣耀V30", "value": "OXF-AN00"}
        ]
    },
    {
        "name": "荣耀",
        "value": "HONOR",
        "models": [
            {"name": "荣耀Magic Vs 至臻版", "value": "FRI-AN10"},
            {"name": "荣耀Magic Vs", "value": "FRI-AN00"},
            {"name": "荣耀Magic V", "value": "MGI-AN00"},
            {"name": "荣耀Magic 5 至臻版", "value": "PGT-AN20"},
            {"name": "荣耀Magic 5 Pro", "value": "PGT-AN10"},
            {"name": "荣耀Magic 5", "value": "PGT-AN00"},
            {"name": "荣耀Magic 4 至臻版", "value": "LGE-AN20"},
            {"name": "荣耀Magic 4 Pro", "value": "LGE-AN10"},
            {"name": "荣耀Magic 4", "value": "LGE-AN00"},
            {"name": "荣耀80 GT", "value": "AGT-AN00"},
            {"name": "荣耀80 Pro", "value": "ANP-AN00"},
            {"name": "荣耀80 Pro 直屏版", "value": "ANB-AN00"},
            {"name": "荣耀80", "value": "ANN-AN00"},
            {"name": "荣耀80 SE", "value": "GIA-AN80"},
            {"name": "荣耀70 Pro+", "value": "HPB-AN00"},
            {"name": "荣耀70 Pro", "value": "SDY-AN00"},
            {"name": "荣耀70", "value": "FNE-AN00"},
            {"name": "荣耀60 Pro", "value": "TNA-AN00"},
            {"name": "荣耀60", "value": "LSA-AN00"},
            {"name": "荣耀X50i", "value": "CRT-AN00"},
            {"name": "荣耀X40 GT", "value": "ADT-AN00"},
            {"name": "荣耀40i", "value": "DIO-AN00"},
            {"name": "荣耀X40", "value": "RMO-AN00"}
        ]
    },
    {
        "name": "小米/Redmi",
        "value": "Xiaomi",
        "models": [
            {"name": "小米13 Ultra", "value": "2304FPN6DC"},
            {"name": "小米13 Pro", "value": "2210132C"},
            {"name": "小米13", "value": "2211133C"},
            {"name": "小米12S Ultra", "value": "2203121C"},
            {"name": "小米12S Pro", "value": "2206122SC"},
            {"name": "小米12S", "value": "2206123SC"},
            {"name": "小米12 Pro", "value": "2201122C"},
            {"name": "小米12", "value": "2201123C"},
            {"name": "小米12X", "value": "2112123AC"},
            {"name": "小米12 Pro 天玑版", "value": "2207122MC"},
            {"name": "小米11 Ultra", "value": "M2102K1C"},
            {"name": "小米11 Pro", "value": "M2102K1AC"},
            {"name": "小米11", "value": "M2011K2C"},
            {"name": "小米11 青春版", "value": "M2101K9C"},
            {"name": "小米11 青春活力版", "value": "2107119DC"},
            {"name": "小米10 至尊纪念版", "value": "M2007J1SC"},
            {"name": "小米10 青春版1", "value": "M2022J9E"},
            {"name": "小米10 青春版2", "value": "M2102J2SC"},
            {"name": "小米10 Pro", "value": "Mi 10 Pro"},
            {"name": "小米10", "value": "Mi 10"},
            {"name": "小米5", "value": "MI 5"},
            {"name": "小米MIX Fold 2", "value": "22061218C"},
            {"name": "小米MIX FOLD", "value": "M2011J18C"},
            {"name": "小米MIX Alpha", "value": "MIX Alpha"},
            {"name": "小米MIX 4", "value": "2106118C"},
            {"name": "小米MIX 3 5G", "value": "Mi MIX 3 5G"},
            {"name": "小米MIX 3 故宫特别版", "value": "MIX 3 The Palace Museum Edition"},
            {"name": "小米MIX 3", "value": "MIX 3"},
            {"name": "小米MIX 2S 翡翠艺术版", "value": "MIX 2S Emerald Edition"},
            {"name": "小米MIX 2S", "value": "MIX 2S"},
            {"name": "小米MIX 2 艺术特别版", "value": "MIX 2 ART"},
            {"name": "小米MIX 2", "value": "MIX 2"},
            {"name": "小米MIX", "value": "MIX"},
            {"name": "小米Civi 3", "value": "23046PNC9C"},
            {"name": "小米Civi 2", "value": "2209129SC"},
            {"name": "小米Civi 1S", "value": "2109119BC"},
            {"name": "小米Civi", "value": "Xiaomi Civi"},
            {"name": "Redmi K60 Pro", "value": "22127RK46C"},
            {"name": "Redmi K60", "value": "23013RK75C"},
            {"name": "Redmi K60E", "value": "22122RK93C"},
            {"name": "Redmi K50 电竞版", "value": "21121210C"},
            {"name": "Redmi K50 至尊版", "value": "22081212C"},
            {"name": "Redmi K50 Pro", "value": "22011211C"},
            {"name": "Redmi K50", "value": "22041211AC"},
            {"name": "Redmi K40S", "value": "22021211RC"},
            {"name": "Redmi K40 游戏增强版", "value": "M2012K10C"},
            {"name": "Redmi K40 Pro", "value": "M2012K11C"},
            {"name": "Redmi K40", "value": "M2012K11AC"},
            {"name": "Redmi Note 12 Turbo", "value": "23049RAD8C"},
            {"name": "Redmi Note 12 Pro 极速版", "value": "22101320C"},
            {"name": "Redmi Note 12 探索版", "value": "22101316UC"},
            {"name": "Redmi Note 12 Pro+", "value": "22101316UCP"},
            {"name": "Redmi Note 12 Pro", "value": "22101316C"},
            {"name": "Redmi Note 12", "value": "22101317C"},
            {"name": "Redmi Note 11T Pro+", "value": "22041216UC"},
            {"name": "Redmi Note 11T Pro", "value": "22041216C"},
            {"name": "Redmi Note 11 Pro+", "value": "21091116UC"},
            {"name": "Redmi Note 11 Pro", "value": "21091116C"},
            {"name": "Redmi Note 11 5G", "value": "21091116AC"},
            {"name": "Redmi Note 11 4G", "value": "21121119SC"},
            {"name": "Redmi Note 11R", "value": "22095RA98C"},
            {"name": "Redmi Note 11E Pro", "value": "2201116SC"}
        ]
    },
    {
        "name": "一加",
        "value": "OnePlus",
        "models": [
            {"name": "OnePlus 11", "value": "PHB110"},
            {"name": "OnePlus 10 Pro", "value": "NE2210"},
            {"name": "OnePlus 9R", "value": "LE2100"},
            {"name": "OnePlus 9RT", "value": "MT2110"},
            {"name": "OnePlus 9 Pro", "value": "LE2120"},
            {"name": "OnePlus 9", "value": "LE2110"},
            {"name": "OnePlus 8T", "value": "KB2000"},
            {"name": "OnePlus 8 Pro", "value": "IN2020"},
            {"name": "OnePlus 8", "value": "IN2010"},
            {"name": "OnePlus 7T Pro", "value": "HD1910"},
            {"name": "OnePlus 7T", "value": "HD1900"},
            {"name": "OnePlus 7 Pro", "value": "GM1910"},
            {"name": "OnePlus 7", "value": "GM1900"},
            {"name": "OnePlus Ace 2V", "value": "PHP110"},
            {"name": "OnePlus Ace 2", "value": "PHK110"},
            {"name": "OnePlus Ace Pro", "value": "PGP110"},
            {"name": "OnePlus Ace 竞速版", "value": "PGZ110"},
            {"name": "OnePlus Ace", "value": "PGKM10"}
        ]
    },
    {
        "name": "OPPO",
        "value": "OPPO",
        "models": [
            {"name": "OPPO Find N2", "value": "PGU100"},
            {"name": "OPPO Find N2 Flip", "value": "PGT100"},
            {"name": "OPPO Find N", "value": "PEUM00"},
            {"name": "OPPO Find X6 Pro", "value": "PGEM10"},
            {"name": "OPPO Find X6", "value": "PGFM10"},
            {"name": "OPPO Find X5 Pro", "value": "PFEM10"},
            {"name": "OPPO Find X5", "value": "PFFM10"},
            {"name": "OPPO Find X3 Pro MARS", "value": "PEEM00_MARS"},
            {"name": "OPPO Find X3 Pro", "value": "PEEM00"},
            {"name": "OPPO Find X3", "value": "PEDM00"},
            {"name": "OPPO Reno9 Pro+", "value": "PGW110"},
            {"name": "OPPO Reno9 Pro", "value": "PGX110"},
            {"name": "OPPO Reno9", "value": "PHM110"},
            {"name": "OPPO Reno8 Pro+", "value": "PFZM10"},
            {"name": "OPPO Reno8 Pro", "value": "PGAM10"},
            {"name": "OPPO Reno8", "value": "PGBM10"},
            {"name": "OPPO K10x", "value": "PGGM10"},
            {"name": "OPPO K10 Pro", "value": "PGIM10"},
            {"name": "OPPO K10", "value": "PGJM10"},
            {"name": "OPPO K9s", "value": "PERM10"},
            {"name": "OPPO K9 Pro", "value": "PEYM00"},
            {"name": "OPPO K9", "value": "PEXM00"},
            {"name": "OPPO A1 Pro", "value": "PHQ110"},
            {"name": "OPPO A1", "value": "PHS110"},
            {"name": "OPPO A97", "value": "PFTM10"},
            {"name": "OPPO A96", "value": "PFUM10"},
            {"name": "OPPO A58", "value": "PHJ110"},
            {"name": "OPPO A57", "value": "PFTM20"},
            {"name": "OPPO A55s", "value": "PEMM00"},
            {"name": "OPPO A36", "value": "PESM10"}
        ]
    },
    {
        "name": "真我",
        "value": "realme",
        "models": [
            {"name": "真我11 Pro+", "value": "RMX3740"},
            {"name": "真我11 Pro", "value": "RMX3770"},
            {"name": "真我11", "value": "RMX3751"},
            {"name": "真我10s", "value": "RMX3617"},
            {"name": "真我10 Pro+", "value": "RMX3687"},
            {"name": "真我10 Pro", "value": "RMX3663"},
            {"name": "真我10", "value": "RMX3615"},
            {"name": "真我GT2大师探索版", "value": "RMX3551"},
            {"name": "真我GT2 Pro", "value": "RMX3300"},
            {"name": "真我GT2", "value": "RMX3310"},
            {"name": "真我GT 大师版", "value": "RMX3361"},
            {"name": "真我Q5 Pro", "value": "RMX3572"},
            {"name": "真我Q5", "value": "RMX3478"},
            {"name": "真我Q5i", "value": "RMX3574"},
            {"name": "真我Q3s", "value": "RMX3461"},
            {"name": "真我Q3t", "value": "RMX3462"},
            {"name": "真我Q3 Pro 狂欢版", "value": "RMX3142"},
            {"name": "真我Q3 Pro", "value": "RMX2205"},
            {"name": "真我Q3", "value": "RMX3161"},
            {"name": "真我Q3i", "value": "RMX3042"},
            {"name": "真我GT Neo5", "value": "RMX3708"},
            {"name": "真我GT Neo5 SE", "value": "RMX3700"},
            {"name": "真我GT Neo3", "value": "RMX3562"},
            {"name": "真我GT Neo 闪速版", "value": "RMX3350"},
            {"name": "真我GT Neo2T", "value": "RMX3357"},
            {"name": "真我GT Neo", "value": "RMX3031"},
            {"name": "真我V30t", "value": "RMX3618"},
            {"name": "真我X7 Pro 至尊版", "value": "RMX3115"},
            {"name": "真我X7 Pro", "value": "RMX2121"},
            {"name": "真我X7", "value": "RMX2176"},
            {"name": "真我X50 Pro 玩家版", "value": "RMX2072"},
            {"name": "真我X50 Pro", "value": "RMX2071"},
            {"name": "真我X50m", "value": "RMX2142"},
            {"name": "真我X50", "value": "RMX2051"}
        ]
    },
    {
        "name": "vivo/iQOO",
        "value": "vivo",
        "models": [
            {"name": "vivo X Fold2", "value": "V2266A"},
            {"name": "vivo X Flip", "value": "V2256A"},
            {"name": "vivo X Fold+", "value": "V2229A"},
            {"name": "vivo X Fold", "value": "V2178A"},
            {"name": "vivo X Note", "value": "V2170A"},
            {"name": "vivo X90 Pro+", "value": "V2227A"},
            {"name": "vivo X90 Pro", "value": "V2242A"},
            {"name": "vivo X90", "value": "V2241A"},
            {"name": "vivo X80 Pro 天玑9000", "value": "V2186A"},
            {"name": "vivo X80 Pro", "value": "V2185A"},
            {"name": "vivo X80", "value": "V2183A"},
            {"name": "vivo S16 Pro", "value": "V2245A"},
            {"name": "vivo S16", "value": "V2244A"},
            {"name": "vivo S16e", "value": "V2239A"},
            {"name": "vivo S15 Pro", "value": "V2207A"},
            {"name": "vivo S15", "value": "V2203A"},
            {"name": "vivo S15e", "value": "V2190A"},
            {"name": "vivo Y78+", "value": "V2271A"},
            {"name": "vivo Y77", "value": "V2219A"},
            {"name": "vivo Y73t", "value": "V2164PA"},
            {"name": "vivo Y55s", "value": "V2164A"},
            {"name": "vivo Y32", "value": "V2158A"},
            {"name": "iQOO 11 Pro", "value": "V2254A"},
            {"name": "iQOO 11", "value": "V2243A"},
            {"name": "iQOO 10 Pro", "value": "V2218A"},
            {"name": "iQOO 10", "value": "V2217A"},
            {"name": "iQOO 9 Pro", "value": "V2172A"},
            {"name": "iQOO 9", "value": "V2171A"},
            {"name": "iQOO 8", "value": "V2136A"},
            {"name": "iQOO 7", "value": "V2049A"},
            {"name": "iQOO Neo7 SE", "value": "V2038A"},
            {"name": "iQOO Neo7 竞速版", "value": "V2232A"},
            {"name": "iQOO Neo7", "value": "V2231A"},
            {"name": "iQOO Neo6 SE", "value": "V2199A"},
            {"name": "iQOO Neo6", "value": "V2196A"},
            {"name": "iQOO Z7x", "value": "V2272A"},
            {"name": "iQOO Z7i", "value": "V2230EA"},
            {"name": "iQOO Z7", "value": "V2270A"},
            {"name": "iQOO Z6x", "value": "V2164KA"},
            {"name": "iQOO Z6", "value": "V2220A"},
            {"name": "iQOO U5x", "value": "V2180GA"},
            {"name": "iQOO U5", "value": "V2165A"},
            {"name": "iQOO U3", "value": "V2061A"},
            {"name": "iQOO U1x", "value": "V2065A"},
            {"name": "iQOO U1", "value": "V2023A"}
        ]
    },
    {
        "name": "魅族",
        "value": "meizu",
        "models": [
            {"name": "魅族20 无界版", "value": "MEIZU 20 Inf"},
            {"name": "魅族20 Pro", "value": "MEIZU 20 Pro"},
            {"name": "魅族20", "value": "MEIZU 20"},
            {"name": "魅族18s Pro", "value": "MEIZU 18s Pro"},
            {"name": "魅族18s", "value": "MEIZU 18s"},
            {"name": "魅族18X", "value": "MEIZU 18X"},
            {"name": "魅族18 Pro", "value": "MEIZU 18 Pro"},
            {"name": "魅族18", "value": "MEIZU 18"},
            {"name": "魅族17 Pro", "value": "meizu 17 Pro"},
            {"name": "魅族17", "value": "meizu 17"}
        ]
    },
    {
        "name": "三星",
        "value": "Samsung",
        "models": [
            {"name": "Galaxy S23 Ultra", "value": "SM-S9180"},
            {"name": "Galaxy S23+", "value": "SM-S9160"},
            {"name": "Galaxy S23", "value": "SM-S9110"},
            {"name": "Galaxy S22 Ultra", "value": "SM-S9080"},
            {"name": "Galaxy S22+", "value": "SM-S9060"},
            {"name": "Galaxy S22", "value": "SM-S9010"},
            {"name": "Galaxy S21 Ultra", "value": "SM-G9980"},
            {"name": "Galaxy S21+", "value": "SM-G9960"},
            {"name": "Galaxy S21", "value": "SM-G9910"},
            {"name": "Galaxy S21 FE", "value": "SM-G9900"},
            {"name": "Galaxy Note20 Ultra", "value": "SM-N9860"},
            {"name": "Galaxy Note20", "value": "SM-N9810"},
            {"name": "Galaxy Note10+", "value": "SM-N9760"},
            {"name": "Galaxy Note10", "value": "SM-N9700"},
            {"name": "Galaxy Z Fold4", "value": "SM-F9360"},
            {"name": "Galaxy Z Fold3", "value": "SM-F9260"},
            {"name": "Galaxy Z Fold2", "value": "SM-F9160"},
            {"name": "Galaxy Fold", "value": "SM-F9000"},
            {"name": "Galaxy Z Flip4", "value": "SM-F7210"},
            {"name": "Galaxy Z Flip3", "value": "SM-F7110"},
            {"name": "Galaxy Z Flip 5G", "value": "SM-F7070"},
            {"name": "Galaxy Z Flip", "value": "SM-F7000"},
            {"name": "W23", "value": "SM-W9023"},
            {"name": "W23 Flip", "value": "SM-W7023"},
            {"name": "W22", "value": "SM-W2022"},
            {"name": "W20", "value": "SM-W2020"},
            {"name": "W21", "value": "SM-W2021"}
        ]
    },
    {
        "name": "华硕/ROG",
        "value": "asus",
        "models": [
            {"name": "ROG 7 Pro", "value": "ASUS_AI2205_B"},
            {"name": "ROG 7", "value": "ASUS_AI2205_A"},
            {"name": "ROG 6 天玑至尊版", "value": "ASUS_AI2203_B"},
            {"name": "ROG 6 天玑版", "value": "ASUS_AI2203_A"},
            {"name": "ROG 6 Pro", "value": "ASUS_AI2201_B"},
            {"name": "ROG 6", "value": "ASUS_AI2201_A"},
            {"name": "ROG 5 幻影", "value": "ASUS_I005DB"},
            {"name": "ROG 5", "value": "ASUS_I005DA"},
            {"name": "ROG 3", "value": "ASUS_I003DD"},
            {"name": "ROG 2", "value": "ASUS_I001DA"},
            {"name": "ROG", "value": "ASUS_Z01QD"},
            {"name": "Smartphone for Snapdragon Insiders", "value": "ASUS_I007D"}
        ]
    },
    {
        "name": "索尼",
        "value": "Sony",
        "models": [
            {"name": "Xperia Pro-I", "value": "XQ-BE72"},
            {"name": "Xperia 1", "value": "J9110"},
            {"name": "Xperia 1 Ⅱ", "value": "XQ-AT72"},
            {"name": "Xperia 1 Ⅲ", "value": "XQ-BC72"},
            {"name": "Xperia 1 Ⅳ", "value": "XQ-CT72"},
            {"name": "Xperia 5", "value": "J9210"},
            {"name": "Xperia 5 Ⅱ", "value": "XQ-AS72"},
            {"name": "Xperia 5 Ⅲ", "value": "XQ-BQ72"},
            {"name": "Xperia 5 Ⅳ", "value": "XQ-CQ72"},
            {"name": "Xperia 10 Plus", "value": "I4293"}
        ]
    },
    {
        "name": "联想/拯救者",
        "value": "Lenovo",
        "models": [
            {"name": "拯救者Y90", "value": "Lenovo L71061"},
            {"name": "拯救者Y70", "value": "Lenovo L71091"},
            {"name": "拯救者2 Pro", "value": "Lenovo L70081"},
            {"name": "拯救者Pro", "value": "Lenovo L79031"},
            {"name": "Lenovo Z6 Pro 5G", "value": "Lenovo L79041"},
            {"name": "Lenovo Z6 Pro", "value": "Lenovo L78051"},
            {"name": "Lenovo Z6", "value": "Lenovo L78121"},
            {"name": "Lenovo Z6 青春版", "value": "Lenovo L38111"},
            {"name": "Lenovo Z5 Pro GT", "value": "Lenovo L78032"},
            {"name": "Lenovo Z5 Pro", "value": "Lenovo L78031"},
            {"name": "Lenovo Z5s", "value": "Lenovo L78071"},
            {"name": "Lenovo Z5", "value": "Lenovo L78011"}
        ]
    },
    {
        "name": "黑鲨",
        "value": "blackshark",
        "models": [
            {"name": "黑鲨5 Pro 中国航天版", "value": "SHARK KTUS-A1"},
            {"name": "黑鲨5 中国航天版", "value": "SHARK PAR-A1"},
            {"name": "黑鲨5 Pro", "value": "SHARK KTUS-A0"},
            {"name": "黑鲨5", "value": "SHARK PAR-A0"},
            {"name": "黑鲨5 RS", "value": "SHARK KSR-A2"},
            {"name": "黑鲨4S 高达版", "value": "SHARK PRS-A2"},
            {"name": "黑鲨4S", "value": "SHARK PRS-A1"},
            {"name": "黑鲨4 Pro", "value": "SHARK KSR-A0"},
            {"name": "黑鲨4", "value": "SHARK PRS-A0"},
            {"name": "黑鲨3S", "value": "SHARK KLE-A1"},
            {"name": "黑鲨3 Pro", "value": "SHARK MBU-A0"},
            {"name": "黑鲨3", "value": "SHARK KLE-A0"},
            {"name": "黑鲨2 Pro", "value": "DLT-A0"},
            {"name": "黑鲨2", "value": "SKW-A0"},
            {"name": "黑鲨Helo", "value": "AWM-A0"},
            {"name": "黑鲨游戏手机", "value": "SKR-A0"}
        ]
    },
    {
        "name": "努比亚/红魔",
        "value": "nubia",
        "models": [
            {"name": "红魔7S Pro 氘锋透明版", "value": "NX709S-TMB"},
            {"name": "红魔7S Pro", "value": "NX709S"},
            {"name": "红魔7S 氘锋透明版", "value": "NX679S-TMB"},
            {"name": "红魔7S", "value": "NX679S"},
            {"name": "红魔7 Pro 透明版", "value": "NX709J-TMB"},
            {"name": "红魔7 Pro", "value": "NX709J"},
            {"name": "红魔7 氘锋透明版", "value": "NX679J-TMB"},
            {"name": "红魔7", "value": "NX679J"},
            {"name": "红魔6S Pro", "value": "NX669S"},
            {"name": "红魔6R", "value": "NX669J-TMB"},
            {"name": "红魔6 Pro", "value": "NX669J-P"},
            {"name": "红魔6", "value": "NX679J"},
            {"name": "努比亚Z50 Ultra", "value": "NX712J"},
            {"name": "努比亚Z50", "value": "NX711J"},
            {"name": "努比亚Z40S Pro", "value": "NX702J"},
            {"name": "努比亚Z40 Pro", "value": "NX701J"},
            {"name": "努比亚Z30 Pro", "value": "NX667J"},
            {"name": "红魔8 Pro+氘锋透明版", "value": "NX729J_V1ATMB"},
            {"name": "红魔8 Pro+", "value": "NX729J_V1A"},
            {"name": "红魔8 Pro氘锋透明版", "value": "NX729J_V2ATMB"},
            {"name": "红魔8 Pro", "value": "NX729J_V2A"},
            {"name": "红魔6R", "value": "NX666J"},
            {"name": "红魔6 Pro氘锋透明版", "value": "NX669J-TMB"}
        ]
    },
    {
        "name": "中兴",
        "value": "ZTE",
        "models": [
            {"name": "Axon 40 Ultra", "value": "ZTE A2023P"},
            {"name": "Axon 40 Pro", "value": "ZTE A2023"},
            {"name": "Axon 30 Ultra", "value": "ZTE A2022P"},
            {"name": "Axon 30 Pro", "value": "ZTE A2022"},
            {"name": "中兴S30", "value": "ZTE 9030N"}
        ]
    },
    {
        "name": "摩托罗拉",
        "value": "motorola",
        "models": [
            {"name": "moto raza 2022", "value": "XT2251-1"},
            {"name": "moto raza 5G", "value": "XT2071-4"},
            {"name": "moto X40", "value": "XT2301-5"},
            {"name": "moto X30 Pro", "value": "XT2241-1"},
            {"name": "moto X30 屏下摄像版", "value": "XT2201-6"},
            {"name": "moto edge X30", "value": "XT2201-2"},
            {"name": "moto edge S30 Pro", "value": "XT2243-2"},
            {"name": "moto edge S30", "value": "XT2175-2"},
            {"name": "moto edge s pro", "value": "XT2153-1"},
            {"name": "moto edge s", "value": "XT2125-4"},
            {"name": "moto edge轻奢版", "value": "XT2143-1"},
            {"name": "moto g53", "value": "XT2335-3"},
            {"name": "moto g71s", "value": "XT2225-2"}
        ]
    }
]


# 获取UA
def get_User_Agent(client_id, device_id, ua_key, timestamp, phoneModel, phoneBuilder, random_version):
    UA = "ANDROID-com.pikcloud.pikpak/" + random_version + " protocolversion/200 accesstype/ clientid/" + client_id + " clientversion/" + random_version + " action_type/ networktype/WIFI sessionid/ deviceid/" + device_id + " providername/NONE devicesign/div101." + ua_key + " refresh_token/ sdkversion/1.1.0.110000 datetime/" + timestamp + " usrno/ appname/android-com.pikcloud.pikpak session_origin/ grant_type/ appid/ clientip/ devicename/" + phoneBuilder.capitalize() + "_" + phoneModel.capitalize() + " osversion/13 platformversion/10 accessmode/ devicemodel/" + phoneModel
    return UA


# 获取ua
def get_user_agent():
    tmp1 = random.randrange(90, 120)
    tmp2 = random.randrange(5200, 5500)
    tmp3 = random.randrange(90, 180)
    tmp_version = str(tmp1) + ".0." + str(tmp2) + "." + str(tmp3)
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + tmp_version + ' Safari/537.36 '
    print(ua)
    return ua


# md5加密算法
def get_hash(str):
    obj = hashlib.md5()
    obj.update(str.encode("utf-8"))
    result = obj.hexdigest()
    return result


# 获取captcha_sign
def get_sign(orgin_str, version):
    # 通过版本号获取对应的salts
    salts = get_random_salts(version)
    if not salts:
        print("无法找到指定版本的salts")
        return None
    print("Salts：" + str(salts))
    for salt in salts:
        orgin_str = get_hash(orgin_str + salt["salt"])
    print("Sign：", orgin_str)
    return orgin_str


def get_random_salts(version):
    # 根据版本号查找对应的salts值
    for v_info in salts_list:
        if v_info["v"] == version:
            return v_info["algorithms"]
    # 如果未找到匹配的版本，返回None或者抛出异常
    return None


# 获取随机获取版本号
def get_random_version():
    version_numbers = [v_info["v"] for v_info in salts_list]
    # 随机选择一个版本号
    random_version = random.choice(version_numbers)
    return random_version


def get_ua_key(device_id):
    rank_1 = hashlib.sha1((device_id + "com.pikcloud.pikpak1appkey").encode("utf-8")).hexdigest()
    rank_2 = get_hash(rank_1)
    return device_id + rank_2


# ============邮箱接口函数，已对接4个临时邮箱接口============
# 临时邮箱2不同后缀的数组
domains2 = ["mailto.plus", "fexpost.com", "fexbox.org", "mailbox.in.ua", "rover.info", "chitthi.in", "fextemp.com",
            "any.pink", "merepost.com"]
# 临时邮箱3-4不同后缀的数组
domains3 = ["nqmo.com", "qabq.com", "end.tw", "uuf.me", "yzm.de"]


def generate_random_name(length=10):
    """生成一个指定长度的随机字符串，包含字母和数字"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


# ============临时邮件 1 获取及接收============

# 获取临时邮箱1最终邮箱名称
def get_email1():
    json_data = {
        "min_name_length": 10,
        "max_name_length": 10
    }
    response = requests.post('https://api.internal.temp-mail.io/api/v3/email/new', json=json_data)
    mail = response.json()['email']
    print(f'获取邮箱:{mail}')
    return mail


# 获取邮箱1的验证码内容
def get_verification_code1(mail):
    for i in range(50):
        res = requests.get(f'https://api.internal.temp-mail.io/api/v3/email/{mail}/messages')
        html = res.json()
        if html:
            text = (html[0])['body_text']
            code = re.search('\\d{6}', text).group()
            print(f'获取邮箱验证码:{code}')
            return code


# ============临时邮件 2 获取及接收============
# 临时邮箱2原本的随机生成规则
def get_random_pre():
    l = 5 + random.randint(0, 2)
    w = ''
    s = ['aeouy', 'bcdfghkmnpqstvwxz']
    t = random.randint(0, 1)
    x = 5 if t else 7
    for i in range(l):
        w += s[t][random.randint(0, len(s[t]) - 1)]

        if random.randint(0, x) > 1:
            t = 1 - t
            x = 5 if t else 10
        else:
            x += 4
    return w


# 获取邮箱2随机名称
def get_email2():
    domain = random.choice(domains2)
    email = get_random_pre() + "@" + domain
    url = "https://tempmail.plus/api/mails?email=" + email + "&first_id=0&epin="
    res = requests.get(url)
    # 返回 email
    print(f'获取邮箱:{email}')
    return email


# 获取随机邮箱的FirstId
def get_email_first_id(email):
    url = "https://tempmail.plus/api/mails?email=" + email + "&first_id=0&epin="
    res = requests.get(url)
    # 得到JSON数据
    data = res.json()
    # 获取 first_id
    first_id = data["first_id"]
    # 返回 first_id
    return first_id


# 获取邮箱2的邮件内容
def get_verification_code2(first_id, email):
    for i in range(50):
        url = f"https://tempmail.plus/api/mails/{first_id}?email={email}&epin="
        res = requests.get(url)
        # 请求成功，处理响应数据
        data = res.json()
        if data:
            # 提取 text 属性的值
            text = data["text"]
            code = re.search('\\d{6}', text).group()
            print(f'获取邮箱验证码:{code}')
            return code


# ============临时邮件 3&4 获取及接收============
# 获取 auth token
def get_authorize_token(domain_suffix):
    api_url = f"https://mail.{domain_suffix}/api/api/v1/auth/authorize_token"
    response = requests.post(api_url)
    if response.status_code == 200:
        # 返回token
        return "Bearer " + response.text.strip('"\n')
    else:
        # 返回错误信息
        return f"Error: {response.status_code}"


# 随机生成临时邮件3&4
def get_email3(auth_token, domain_suffix):
    name = generate_random_name()
    domain = random.choice(domains3)
    email = name + "@" + domain
    api_url = f"https://mail.{domain_suffix}/api/api/v1/mailbox/{email}"
    headers = {
        "Authorization": auth_token
    }
    requests.get(api_url, headers=headers)
    # 返回 email
    print(f'获取邮箱验证码:{email}')
    return email


# 获取email的邮件ID
def get_email_id(email, auth_token, domain_suffix):
    api_url = f"https://mail.{domain_suffix}/api/api/v1/mailbox/{email}"
    headers = {
        "Authorization": auth_token
    }
    res = requests.get(api_url, headers=headers)
    data = res.json()
    return data[0]['id']


# 获取临时邮箱3&4的验证码
def get_verification_code3(email_id, email, auth_token, domain_suffix):
    for i in range(50):
        api_url = f"https://mail.{domain_suffix}/api/api/v1/mailbox/{email}/{email_id}/"
        headers = {"Authorization": auth_token}
        res = requests.get(api_url, headers=headers)
        # 请求成功，处理响应数据
        data = res.json()
        if data:
            # 提取 text 属性的值
            text = data.get("body", {}).get("text", "Text content not available")
            code = re.search('\\d{6}', text).group()
            print(f'获取邮箱验证码:{code}')
            return code


# ============临时邮件 5 获取及接收============
# 获取邮箱后缀
def get_mail5_domains(domain_suffix):
    api_url = f"https://api.mail.{domain_suffix}/domains"
    res = requests.get(api_url)
    domains_data = res.json()
    # 取出邮箱后缀
    # Extract domain values and store them in a list
    domain_list = [domain["domain"] for domain in domains_data["hydra:member"]]
    # 判断domain_list是否为空数组，如果是则终止程序
    if not domain_list:
        print("无可用邮箱后缀，请切换其他临时邮箱...")
        return

    return domain_list


# 创建临时邮件 5的账户
def get_email5(domain_suffix):
    domains = get_mail5_domains(domain_suffix)
    random_domain = random.choice(domains)
    address = generate_random_name() + "@" + random_domain
    password = ''.join(random.choice(string.digits) for _ in range(4))
    data = {"address": address, "password": password}
    api_url = f"https://api.mail.{domain_suffix}/accounts"
    response = requests.post(api_url, json=data)
    if response.status_code == 201:
        # Add the "password" field
        account_data = response.json()
        account_data["password"] = password
        print(f'获取邮箱:{account_data["address"]}')
        return account_data
    else:
        return None


# 获取账户 token
def get_authorize_token5(email5_obj, domain_suffix):
    if email5_obj:
        token_url = f"https://api.mail.{domain_suffix}/token"
        response = requests.post(token_url, json=email5_obj)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["token"]
            return f"Bearer {token}"
        else:
            return None  # or handle error
    else:
        return None


# 获取验证码
def get_verification_code5(token, domain_suffix):
    url = f"https://api.mail.{domain_suffix}/messages"
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    for i in range(50):
        for message in data["hydra:member"]:
            intro = message["intro"]
            # 使用正则表达式匹配验证码
            match = re.search(r"验证码：\s*(\d+)\s", intro)
            if match:
                captcha = match.group(1)
                print(f'获取邮箱验证码:{captcha}')
                return captcha  # 返回匹配到的第一个验证码


# ============全部网络请求============


# 初始化人机验证网页
# url,captcha_token,expires_in
def part2(client_id, captcha_token, device_id, captcha_sign, email, timestamp, User_Agent, random_version):
    import requests

    url = "https://user.mypikpak.com/v1/shield/captcha/init"

    querystring = {"client_id": client_id}

    payload = {
        "action": "POST:/v1/auth/verification",
        "captcha_token": captcha_token,
        "client_id": client_id,
        "device_id": device_id,
        "meta": {
            "captcha_sign": "1." + captcha_sign,
            "user_id": "",
            "package_name": "com.pikcloud.pikpak",
            "client_version": random_version,
            "email": email,
            "timestamp": timestamp
        },
        "redirect_uri": "xlacc8sdk01://xbase.cloud/callback?state=harbor"
    }
    headers = {
        "X-Device-Id": device_id,
        "User-Agent": User_Agent,
    }
    headers.update(basicRequestHeaders_1)

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 获取图片列表
# pid,traceid,frames,result
def part3(device_id, user_agent, referer):
    import requests

    url = "https://user.mypikpak.com/pzzl/gen"

    querystring = {"deviceid": device_id, "traceid": ""}

    headers = {
        "Host": "user.mypikpak.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": user_agent,
        "referer": referer,
    }
    headers.update(basicRequestHeaders_2)

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 验证图片序号
# result
def part4(pid, device_id, trace_id, f, n, p, a, c, referer, user_agent):
    import requests

    url = "https://user.mypikpak.com/pzzl/verify"

    querystring = {"pid": pid,
                   "deviceid": device_id, "traceid": trace_id, "f": f,
                   "n": n, "p": p, "a": a, "c": c}

    headers = {
        "Host": "user.mypikpak.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": user_agent,
        "referer": referer,
    }
    headers.update(basicRequestHeaders_2)

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 发送验证码
# code,captcha_token,expires_in
def part5(device_id, captcha_token, pid, trace_id, user_agent, referer):
    import requests

    url = "https://user.mypikpak.com/credit/v1/report"

    querystring = {"deviceid": device_id,
                   "captcha_token": captcha_token,
                   "type": "pzzlSlider", "result": "0", "data": pid,
                   "traceid": trace_id}

    headers = {
        "Host": "user.mypikpak.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": user_agent,
        "referer": referer,
    }
    headers.update(basicRequestHeaders_2)
    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 验证验证码1
# verification_id,expires_in,slected_channel
def part6(client_id, captcha_token, email, device_id, User_Agent):
    import requests

    url = "https://user.mypikpak.com/v1/auth/verification"

    querystring = {"client_id": client_id}

    payload = {
        "captcha_token": captcha_token,
        "email": email,
        "locale": "zh-CN",
        "target": "ANY",
        "client_id": client_id
    }
    headers = {
        "X-Device-Id": device_id,
        "User-Agent": User_Agent,
    }
    headers.update(basicRequestHeaders_1)

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 验证验证码2
# verification_token,expires_in
def part8(client_id, verification_id, verification_code, device_id, User_Agent):
    import requests

    url = "https://user.mypikpak.com/v1/auth/verification/verify"

    querystring = {"client_id": client_id}

    payload = {
        "client_id": client_id,
        "verification_id": verification_id,
        "verification_code": verification_code
    }
    headers = {
        "X-Device-Id": device_id,
        "User-Agent": User_Agent,
    }
    headers.update(basicRequestHeaders_1)

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 安全验证
# captcha_token,expires_in
def part8_1(client_id, captcha_token, device_id, captcha_sign, email, timestamp, User_Agent, random_version):
    import requests

    url = "https://user.mypikpak.com/v1/shield/captcha/init"

    querystring = {"client_id": client_id}

    payload = {
        "action": "POST:/v1/auth/signup",
        "captcha_token": captcha_token,
        "client_id": client_id,
        "device_id": device_id,
        "meta": {
            "captcha_sign": "1." + captcha_sign,
            "user_id": "",
            "package_name": "com.pikcloud.pikpak",
            "client_version": random_version,
            "email": email,
            "timestamp": timestamp
        },
        "redirect_uri": "xlaccsdk01://xbase.cloud/callback?state=harbor"
    }
    headers = {
        "Host": "user.mypikpak.com",
        "x-device-id": device_id,
        "user-agent": User_Agent,
        "accept-language": "zh",
        "content-type": "application/json",
        "accept-encoding": "gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 注册账号
# access_token,expires_in,sub
def part9(client_id, captcha_token, client_secret, email, name, password, verification_token, device_id, User_Agent):
    import requests

    url = "https://user.mypikpak.com/v1/auth/signup"

    querystring = {"client_id": client_id}

    payload = {
        "captcha_token": captcha_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "email": email,
        "name": name,
        "password": password,
        "verification_token": verification_token
    }
    headers = {
        "X-Device-Id": device_id,
        "User-Agent": User_Agent,
    }
    headers.update(basicRequestHeaders_1)

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


# 安全验证
# captcha_token,expires_in
def part10(client_id, captcha_token, device_id, captcha_sign, user_id, timestamp, User_Agent, random_version):
    import requests

    url = "https://user.mypikpak.com/v1/shield/captcha/init"

    querystring = {"client_id": client_id}

    payload = {
        "action": "POST:/vip/v1/activity/invite",
        "captcha_token": captcha_token,
        "client_id": client_id,
        "device_id": device_id,
        "meta": {
            "captcha_sign": "1." + captcha_sign,
            "user_id": user_id,
            "package_name": "com.pikcloud.pikpak",
            "client_version": random_version,
            "timestamp": timestamp
        },
        "redirect_uri": "xlaccsdk01://xbase.cloud/callback?state=harbor"
    }
    headers = {
        "X-Device-Id": device_id,
        "User-Agent": User_Agent,
    }
    headers.update(basicRequestHeaders_1)

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)


def one_invite(user_id, phoneModel, phoneBuilder, invite_code, captcha_token, device_id, access_token, User_Agent,
               random_version):
    import requests

    url = "https://api-drive.mypikpak.com/vip/v1/activity/invite"

    payload = {
        "data": {
            "sdk_int": "33",
            "uuid": device_id,
            "userType": "1",
            "userid": user_id,
            "userSub": "",
            "product_flavor_name": "cha",
            "language_system": "zh-CN",
            "language_app": "zh-CN",
            "build_version_release": "13",
            "phoneModel": phoneModel,
            "build_manufacturer": phoneBuilder,
            "build_sdk_int": "33",
            "channel": "official",
            "versionCode": "10150",
            "versionName": random_version,
            "installFrom": "other",
            "country": "PL"
        },
        "apk_extra": {"channel": "official"}
    }
    headers = {
        "Host": "api-drive.mypikpak.com",
        "authorization": "Bearer " + access_token,
        "product_flavor_name": "cha",
        "x-captcha-token": captcha_token,
        "x-client-version-code": "10150",
        "x-device-id": device_id,
        "user-agent": User_Agent,
        "country": "PL",
        "accept-language": "zh-CN",
        "x-peer-id": device_id,
        "x-user-region": "2",
        "x-system-language": "zh-CN",
        "x-alt-capability": "3",
        "accept-encoding": "gzip",
        "content-type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


# 邀请码填写
def part_invite(user_id, phoneModel, phoneBuilder, invite_code, captcha_token, device_id, access_token, User_Agent):
    import requests

    url = "https://api-drive.mypikpak.com/vip/v1/order/activation-code"

    payload = {"activation_code": invite_code}
    headers = {
        "Host": "api-drive.mypikpak.com",
        "authorization": "Bearer " + access_token,
        "product_flavor_name": "cha",
        "x-captcha-token": captcha_token,
        "x-client-version-code": "10150",
        "x-device-id": device_id,
        "user-agent": User_Agent,
        "country": "DK",
        "accept-language": "zh-CN",
        "x-peer-id": device_id,
        "x-user-region": "2",
        "x-system-language": "zh-CN",
        "x-alt-capability": "3",
        "content-length": "30",
        "accept-encoding": "gzip",
        "content-type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


def part11(user_id, phoneModel, phoneBuilder, invite_code, captcha_token, device_id, access_token, User_Agent,
           random_version):
    import requests

    url = "https://api-drive.mypikpak.com/vip/v1/activity/invite"

    payload = {
        "data": {
            "sdk_int": "33",
            "uuid": device_id,
            "userType": "1",
            "userid": user_id,
            "userSub": "",
            "product_flavor_name": "cha",
            "language_system": "zh-CN",
            "language_app": "zh-CN",
            "build_version_release": "13",
            "phoneModel": phoneModel,
            "build_manufacturer": phoneBuilder,
            "build_sdk_int": "33",
            "channel": "spread",
            "versionCode": "10142",
            "versionName": random_version,
            "installFrom": "other",
            "country": "NO"
        },
        "apk_extra": {
            "channel": "spread",
            "invite_code": invite_code
        }
    }
    headers = {
        "Host": "api-drive.mypikpak.com",
        "authorization": "Bearer " + access_token,
        "product_flavor_name": "cha",
        "x-captcha-token": captcha_token,
        "x-client-version-code": "10142",
        "x-device-id": device_id,
        "user-agent": User_Agent,
        "country": "NO",
        "accept-language": "zh-CN",
        "x-peer-id": device_id,
        "x-user-region": "2",
        "x-system-language": "zh-CN",
        "x-alt-capability": "3",
        "accept-encoding": "gzip",
        "content-type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


# 程序运行主函数
mail_token = None
mail_url = None


def start():
    global mail_token, mail_url
    invite_code = input("请输入你的账号邀请码：")

#     invite_code = "97207615"
#     invite_code = "28514441"

    #invite_code = "84150438"
    email_code = input("输入要使用的临时邮箱(1-6)：")
    client_id = "YNxT9w7GMdWvEOKa"
    device_id = str(uuid.uuid4()).replace("-", "")
    timestamp = str(int(time.time()) * 1000)
    random_version = get_random_version()
    print(f'本次随机版本号为:{random_version}')
    if not email_code:
        # 如果没有输入，则随机赋值2-6
        email_code = str(random.randint(2, 6))
        print("本次临时邮箱随机使用:", email_code)
    if email_code == "1":
        email = get_email1()
    elif email_code == "2":
        email = get_email2()
    elif email_code == "3":
        mail_url = "cx"
        mail_token = get_authorize_token(mail_url)
        email = get_email3(mail_token, mail_url)
    elif email_code == "4":
        mail_url = "td"
        mail_token = get_authorize_token(mail_url)
        email = get_email3(mail_token, mail_url)
    elif email_code == "5":
        mail_url = "gw"
        email5_obj = get_email5(mail_url)
        email = email5_obj["address"]
        mail_token = get_authorize_token5(email5_obj, mail_url)
    else:
        mail_url = "tm"
        email5_obj = get_email5(mail_url)
        email = email5_obj["address"]
        mail_token = get_authorize_token5(email5_obj, mail_url)
    org_str = client_id + random_version + "com.pikcloud.pikpak" + device_id + timestamp
    captcha_sign = get_sign(org_str, random_version)
    print(captcha_sign)

    # 获取 UA
    product_index = get_random_number(len(ua_list))
    model_index = get_random_number(len(ua_list[product_index]["models"]))
    phoneModel = ua_list[product_index]["models"][model_index]["value"]
    phoneBuilder = ua_list[product_index]["value"]
    # print(f'随机phoneModel:{phoneModel}')
    # print(f'随机phoneBuilder:{phoneBuilder}')
    ua_key = get_ua_key(device_id)
    User_Agent = get_User_Agent(client_id, device_id, ua_key, timestamp, phoneModel, phoneBuilder, random_version)
    user_agent = get_user_agent()
    time.sleep(1)
    action2 = part2(client_id, "", device_id, captcha_sign, email, timestamp, user_agent, random_version)

    # pid,traceid,frames,result
    action3 = part3(device_id, user_agent, action2['url'])

    select_id = list_compare(action3['frames'])
    img_data = img_secret(action3['frames'], select_id, action3['pid'])
    print(img_data)

    # result
    action4 = part4(action3['pid'], device_id, action3['traceid'], img_data['f'], img_data['ca'][0], img_data['ca'][1],
                    img_data['ca'][2], img_data['ca'][3], action2['url'], user_agent)
    time.sleep(1)
    # code,captcha_token,expires_in
    action5 = part5(device_id, action2["captcha_token"], action3['pid'], action3['traceid'], user_agent, action2['url'])

    # verification_id,expires_in,slected_channel
    action6 = part6(client_id, action5["captcha_token"], email, device_id, user_agent)

    if email_code == "2":
        # 此处sleep可以根据实际情况增加
        time.sleep(3)
        # 获取 first_id
        first_id = get_email_first_id(email)
        # 获取验证码
        verification_code = get_verification_code2(first_id, email)
    elif email_code == "3" or email_code == "4":
        # 此处sleep可以根据实际情况增加
        time.sleep(3)
        # 获取 email_id
        email_id = get_email_id(email, mail_token, mail_url)
        # 获取验证码
        verification_code = get_verification_code3(email_id, email, mail_token, mail_url)
    elif email_code == "5" or email_code == "6":
        # 此处sleep可以根据实际情况增加
        time.sleep(2)
        # 获取验证码
        verification_code = get_verification_code5(mail_token, mail_url)
    else:
        # 执行临时邮箱1
        time.sleep(2)
        verification_code = get_verification_code1(email)

    # verification_token,expires_in
    action8 = part8(client_id, action6['verification_id'], verification_code, device_id, User_Agent)

    timestamp = str(int(time.time()) * 1000)
    org_str = client_id + random_version + "com.pikcloud.pikpak" + device_id + timestamp
    captcha_sign = get_sign(org_str, random_version)
    User_Agent = get_User_Agent(client_id, device_id, ua_key, timestamp, phoneModel, phoneBuilder, random_version)

    action8_1 = part8_1(client_id, action2["captcha_token"], device_id, captcha_sign, email, timestamp, User_Agent,
                        random_version)
    client_secret = "dbw2OtmVEeuUvIptb1Coyg"
    time.sleep(1)
    # access_token,expires_in,sub
    # 账号的昵称设置
    name = email.split("@")[0]
    # 账号的密码设置
    password = "pwd123456"
    action9 = part9(client_id, action8_1['captcha_token'], client_secret, email, name, password,
                    action8['verification_token'], device_id, User_Agent)
    time.sleep(1)
    # captcha_token,expires_in
    action10 = part10(client_id, action8_1['captcha_token'], device_id, captcha_sign, action9['sub'], timestamp,
                      User_Agent, random_version)

    # 邀请填写
    one_invite(action9['sub'], phoneModel, phoneBuilder, invite_code, action10['captcha_token'], device_id,
               action9['access_token'], User_Agent, random_version)
    part_invite(action9['sub'], phoneModel, phoneBuilder, invite_code, action10['captcha_token'], device_id,
                action9['access_token'], User_Agent)

    print("One invitation completes !!!")
    print("Email：", email)
    print("PWD：", password)


if __name__ == '__main__':
    print('注意事项：')
    print('1、邀请源码仅供小伙伴们交流学习，严禁用于牟取任何不正当利益。')
    print('2、代码底层架构较老，可以对程序进行二改升级。')
    print('3、二改的代码外部分享时必须标注原架构开发者【B站-纸鸢花的花语】。')
    print('4、以上事项违反或无视者均无权使用或二改邀请源码。')
    print('5、脚本二改已有6个随机邮箱接口和邮箱后缀，脚本修改作者：https://github.com/LiJunYi2。')
    print('6、临时邮箱分流规则：https://sourl.cn/N6mSik')
    print('7、20240428更新，新增多个设备值及多个PikPak版本Salts值，感谢原作者的教程视频！')
    print('8、输入1-6，不输入则随机选择2-6临时邮箱。')
    start()
    input('程序运行结束')
