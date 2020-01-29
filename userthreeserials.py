import requests
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcsl_v1_5
import base64
import urllib.parse
import json
from Crypto.Hash import SHA1
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

# 激活用户12张card
js_bags={
    "one":{"cardId":"lucky_bag_one","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "two":{"cardId":"lucky_bag_two","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "three":{"cardId":"lucky_bag_three","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "four":{"cardId":"lucky_bag_four","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "five":{"cardId":"lucky_bag_five","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "six":{"cardId":"lucky_bag_six","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "seven":{"cardId":"lucky_bag_seven","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "eight":{"cardId":"lucky_bag_eight","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "nine":{"cardId":"lucky_bag_nine","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "ten":{"cardId":"lucky_bag_ten","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "eleven":{"cardId":"lucky_bag_eleven","serialId":None,"activityCode":"qb_spring_lucky_bag"},
    "twelve":{"cardId":"lucky_bag_twelve","serialId":None,"activityCode":"qb_spring_lucky_bag"}

}
js_usertoken=[]
with open('userthreetoken.txt','r') as f:
    for i in f.readlines()[-3:]:
        js_usertoken.append(json.loads(i.strip()))
print(js_usertoken)


# for i in bags.values():
#     print(i)
#     print(len(i))
#     print(json.dumps(i,separators=(',',':')))
#     print(len(json.dumps(i,separators=(',',':'))))

def getonecard(userinfo,cardinfo):
    sendCardUrl="https://oapi.9f.cn/transformers/lucky/bag/querySendCard/qb_happy_reunion_chinese_year"

# data={"cardId":"lucky_bag_one","serialId":None,"activityCode":"qb_spring_lucky_bag"}
    aeskey = userinfo['token'][:16].encode()
# aeskey = b'15150300fac20100'
    aesiv=b'21520baeed8a48eb'
    cipher = AES.new(aeskey, AES.MODE_CBC,aesiv)
    str_cardinfo=json.dumps(cardinfo,separators=(',',':'))
    print(len(str_cardinfo))
    print(str_cardinfo)
    en_str_cardinfo_bytes = cipher.encrypt(pad(str_cardinfo.encode(), AES.block_size))
    #对结果手动b64处理，否则直接decode报错，
    en_str_cardinfo = base64.b64encode(en_str_cardinfo_bytes).decode('utf-8')

    timestamp=int(round(time.time()*1000))
# print(timestamp)
    sign=str(timestamp)+en_str_cardinfo
    sha1=SHA1.new()
    sha1.update(sign.encode())
    sign=sha1.hexdigest().upper()
    print("sign::::"+sign)

    head_1={
        "Content-Type": "application/json; charset=UTF-8",
        "channel":"QB",
        "memberId":userinfo['memberId'],
       # "Referer": "https://h5.9f.cn/bfe/integrate-act/golden-rat/index.html",
       # "loginChannel":"APP",
        "token":userinfo['token'],
        "sign":sign
    }
    body_1={
        "data":en_str_cardinfo,
        "timestamp":timestamp
    }
    res=requests.post(sendCardUrl,data=json.dumps(body_1),headers=head_1)
    serialId=json.loads(res.text)['data']['serialId']
    print(serialId)
    return {"serialId":serialId,"activityCode":"qb_spring_lucky_bag"}
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")



#获取一个账号12个serialnumber

serialId=[]
for index in range(3):
    for i in js_bags.values():
        serialId.append(getonecard(js_usertoken[index],i))
    print(serialId)
    with open('userthreeserials.txt','a') as f1:
        f1.write(json.dumps({js_usertoken[index]['mobile']:serialId})+'\n')
    serialId=[]

#获取3个号的12个serialId