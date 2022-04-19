import json
import time

import requests

loginurl ='http://hmgr.sec.lit.edu.cn/wms/healthyLogin'
uploadurl = 'http://hmgr.sec.lit.edu.cn/wms/addHealthyRecord'

headers ={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
"Content-Type": "application/json"}

data = {
        "cardNo": "B21043925",
        "password": "b6c3c76ec8b95e67716188ca4488604d2d301b4804ded435dfedb08399e2f1ab"}

# 登录
def gettoken(data):
    res = requests.post(url=loginurl,headers=headers,data=json.dumps(data))

    if res.status_code ==200:
        print("登录")
        print("请求成功:打印返回内容及token")
        s=json.loads(res.text)
        print(s)
        print(s["data"]["token"])
    else:
        print('请求失败')
    with open('./登录.json', 'w') as fp:
        json.dump(res.text, fp)
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
    print(headers)
    print(time.strftime("%Y-%m-%d", time.localtime()))
    updata["reportDate"] = time.strftime("%Y-%m-%d", time.localtime())
    res = requests.post(url=uploadurl,headers=headers,data=json.dumps(updata))
    print(json.dumps(updata))
    if res.status_code==200:
        print("提交成功")
        print(res.text)
    else:
        print('提交失败')


upload()
