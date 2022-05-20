# -*- coding: utf-8 -*-
# @Time    : 2022/4/22 09:01
# @Author  : JingBW
# @Site    : 
# @File    : test06_testAccount.py
# @Software: PyCharm
import json
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

import requests

#可以正常打卡

loginurl ='http://hmgr.sec.lit.edu.cn/wms/healthyLogin'
uploadurl = 'http://hmgr.sec.lit.edu.cn/wms/addHealthyRecord'

headers ={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
"Content-Type": "application/json"}

data = {
        "cardNo": "",
        "password": ""}

# 用户列表，在这里补充用户名，密码，email.SHA256加密后的密码
#下面都是账号都是错误 演示示例而已
userlist =[{
    "username": "B2192",
    "password": "b6c3c4d2d301b4804ded435dfedb08399e2f1ab",
    "email"   : "7861@qq.com"
}
    # ,
    # {
    # "username": "B24533",
    # "password": "bf2365cd2bf0e58ffb26ec5f59b0f174e68b34d3ab8fd9e64",
    # "email"   : "5138@qq.com"
    # },
    # {
    #     "username": "B2926",
    #     "password": "e7752534505f5cc9080d5ea0bc71ff55a8467",
    #     "email": "2591@qq.com"
    # }
]

# 登录
def gettoken(data):
    res = requests.post(url=loginurl,headers=headers,data=json.dumps(data))

    if res.status_code ==200:
        print("登录")
        print("请求成功:打印返回内容及token")
        s=json.loads(res.text)
        # print(s)
        print(s["data"]["token"])
    else:
        print('请求失败')
    # with open('./登录.json', 'w') as fp:
    #     json.dump(res.text, fp)
    return s


# 提交
def upload():
    updata = {
    "abroadInfo": "",
    "caseAddress": None,
    "contactAddress": "",
    "contactCity": "",
    "contactDistrict": "",
    "contactPatient": "1000904",
    "contactProvince": "",
    "contactTime": None,
    "cureTime": None,
    "currentAddress": "洛阳理工学院",
    "currentCity": "410300",
    "currentDistrict": "410311",
    "currentProvince": "410000",
    "currentStatus": "1000705",
    "diagnosisTime": None,
    "exceptionalCase": 0,
    "exceptionalCaseInfo": "",
    "friendHealthy": 0,
    "goHuBeiCity": "",
    "goHuBeiTime": None,
    "healthyStatus": 0,
    "isAbroad": 0,
    "isInTeamCity": 1,
    "isTrip": 0,
    "isolation": 0,
    "mobile": "",
    "peerAddress": "",
    "peerIsCase": 0,
    "peerList": [],
    "reportDate": "",
    "seekMedical": 0,
    "seekMedicalInfo": "",
    "selfHealthy": 0,
    "selfHealthyInfo": "",
    "selfHealthyTime": None,
    "teamId": 3,
    "temperature": "36.6",
    "temperatureNormal": 0,
    "temperatureThree": "",
    "temperatureTwo": "",
    "travelPatient": "1000803",
    "treatmentHospitalAddress": "",
    "tripList": [],
    "userId": "",
    "villageIsCase": 0
    }


    s = gettoken(data)
    headers["token"]=s["data"]["token"]
    updata["mobile"] = s["data"]["mobile"]
    updata["userId"]=s["data"]["userId"]
    updata["teamId"] = s["data"]["teamId"]
    print("打印修改后的header和updata")
    # print(headers)
    print(time.strftime("%Y-%m-%d", time.localtime()))
    updata["reportDate"] = time.strftime("%Y-%m-%d", time.localtime())
    res = requests.post(url=uploadurl,headers=headers,data=json.dumps(updata))
    print(json.dumps(updata))
    re=[]
    if res.status_code==200:
        print("提交成功")
        # print(res.text)
        re.append('提交成功')
        re.append(res.text)

    else:
        print('提交失败')
        re.append('提交失败')
    return re



def mail(receivers,content):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "jingbw"  # 用户名
    mail_pass = "xxxxxxi"  # 口令
    sender = 'xxxxxx@qq.com' #发送邮件账号
    receivers = receivers # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # message = MIMEText(str(s['data']['list'][15]), 'plain', 'utf-8')
    message = MIMEText(str(content[2])+','+str(content[0]), 'plain', 'utf-8')
    message['From'] = Header("Jing", 'utf-8')
    message['To'] = Header(str(content[2]), 'utf-8')

    subject = "健康汇报,"+content[0]
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except Exception:
        print("Error: 无法发送邮件")



def main(event, context):
    for i in range(len(userlist)):
        data['cardNo'] = userlist[i]['username']
        data['password'] = userlist[i]['password']
        re=[userlist[i]['username'],'账号错误','账号错误']
        try:
            re = upload()
        except Exception:
            print(userlist[i]['username'],'账号运行异常')
        stuId=userlist[i]['username']
        re.append(stuId)
        mail(userlist[i]['email'], re)
        print(stuId,",打卡完成。")
        print("Received context: " + str(context))


if __name__ == '__main__':
    main(event='',context='')
