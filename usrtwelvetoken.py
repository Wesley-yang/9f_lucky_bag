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


def gettoken(user):
    public_key = '''-----BEGIN PUBLIC KEY-----
    MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAOAvi4p9BUpNeXgXyNLM1uSnK4uIvfREAM72lhb5MwHmfO6FD7SyId1auo3JtCEG8oUS6AKYmxcTGj+yrI728G0CAwEAAQ==
    -----END PUBLIC KEY-----
    '''
    a='a'.encode()
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pkcsl_v1_5.new(rsakey)
    password = base64.b64encode(cipher.encrypt(a)).decode()
    # print("rsa密码：：：" + password)
    url = "https://api3.9f.cn/phoenix/app/v4/member/encrypt/login"
    head = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://h5.9f.cn/bfe/9f-act/msite-login/index.html",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }
    body = {"data": {
        "token": "", "memberId": "", "versionCode": 493, "versionName": "4.9.3",
        "timestamp": int(round(time.time() * 1000)), "platform": "h5",
        "model": {"mobile": user, "password": password}}}

    data = urllib.parse.urlencode(body)
    res = requests.post(url, data=data, headers=head)
    token = json.loads(res.text)['model']['token']
    memberId = json.loads(res.text)['model']['memberId']
    mobile=json.loads(res.text)['model']['mobile']
    # print("token     " + token + "   Id     " + memberId)
    return {"mobile":mobile,"token":token,"memberId":memberId}


userlist=[]
usertoken=[]
with open('user.txt','r') as f:
    for line in f.readlines()[:-1]:
        userlist.append(line.strip())
print(userlist)

for index,user in enumerate(userlist):
    print(index)
    txt=json.dumps(gettoken(user))
    with open('usertoken.txt','a') as f:
        f.write(txt+'\n')




