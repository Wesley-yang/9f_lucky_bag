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

usertoken=[]
with open('usertoken.txt','r') as f:
    for i in f.readlines()[-12:]:
        usertoken.append(json.loads(i.strip()))
print(usertoken)

userserialId=[]
with open('userthreeserials.txt','r') as f1:
    for i in f1.readlines()[-3:]:
        for h in json.loads(i).values():
            userserialId.append(h)
print(userserialId)
#[[{1},{2},{3}],[{1}{2}{3}],[{1}{2}{3}]]
def activecard(userinfo,cardinfo):
    active_url="https://oapi.9f.cn/transformers/lucky/bag/inviteeUserOpenPacket/qb_happy_reunion_chinese_year"
# userinfo,dic_类型={"mobile": "17854216528", "token": "15150300a1d400005a3d29fda9214b5ba6186cfce71c796d", "memberId": "1004053514"}
# cardinfo,dic_类型={"serialId":"158025324475935111577","activityCode":"qb_spring_lucky_bag"}
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
    res=requests.post(active_url,data=json.dumps(body_1),headers=head_1)
    serialId=json.loads(res.text)
    print(serialId)
    # return serialId
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


for index,user in enumerate(usertoken):
    print(index)
    # print(type(json.loads(user)))
    print(user)
    for b in userserialId:
        activecard(user,b[index])
#拆3个号共36个福袋
