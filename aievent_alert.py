import time
import datetime
import requests
import os,sys, os.path
import shutil
import json
from pathlib import Path 
import base64
from datetime import timedelta
from aialertconfig import AIAlertConfig
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.auth import HTTPBasicAuth 

class AIEvent_Alert():
    def __init__(self,callback_func):
        self.callback_func=callback_func
        try :
            with open("AIAlert_default.json", "r") as jsonFile:
                self.defaultAlert = json.load(jsonFile)
        except :   
            print("Cannot load default alert json file!!!")
    def time_stamp(self):
	    timestamp = int(time.time() * 1000)
	    return timestamp
    def EventAlertJsonSend(self,imgfile):
        image = open(imgfile, 'rb')#open binary file in read mode
        #image = open(imgphysicalpathdownsize, 'rb')#open binary file in read mode
        ENCODING = 'utf-8'
        image_read = image.read() 
        image_64_encode = base64.b64encode(image_read) 
        bimdata = {"b64img": image_64_encode.decode(ENCODING) }
        tempimg64 = image_64_encode.decode(ENCODING)     
        cdata= self.defaultAlert
        cdata["timestamp"]=str(datetime.datetime.now())
        cdata["image"]=tempimg64
        cdata["faceImage"]=tempimg64
        try:
            response = requests.post(AIAlertConfig.API_POST_URL, data=json.dumps(cdata),headers={'Content-Type': 'application/json'}, timeout=(10, 15))
            print("Server url : "+ AIAlertConfig.API_POST_URL)
            print(response.status_code)
            print(response.text)
        except Exception as e:
            print ("Exception in EventAlertSend  {0} ".format(e))

    def EventAlertMultipartSend(self,imgfile):
        sess = requests.Session()
        r = sess.get(AIAlertConfig.LOGIN_POST_URL)
        print(r.status_code)
        #print(r.text)
        ###login
        my_csrf_token = r.cookies['csrftoken']
        login_data = dict(username="admin", password="admin", csrfmiddlewaretoken=my_csrf_token, next='/admin/ai_event/ai_event/add/')
        #login_data = dict(username="admin", password="admin", next='/admin/ai_event/ai_event/add/') , headers=dict(Referer=AIAlertConfig.ADD_EVENT_POST_URL)
        r  = sess.post(AIAlertConfig.LOGIN_POST_URL, data=login_data)
        print("Login reposne:{0}".format(r.status_code))
        #print(r.text)
        time.sleep(2)
        r=sess.get(AIAlertConfig.ADD_EVENT_POST_URL)
        print("request:Get reposne:{0}".format(r.status_code))
        #print(r.text)        
        csrftoken2 = r.cookies['csrftoken']
        #send Multipart
        multipart_data = MultipartEncoder(fields={
            "csrfmiddlewaretoken": csrftoken2,
            "category":"RogerDog",
            "subcategory":"moto",
            "location":"camera",
            "floor":"l3",
            "camera":"camera02",
            "timestamp_0":"2021-03-07",
            "timestamp_1":"18:40:30",
            "initial-timestamp_0":"2021-03-07",
            "initial-timestamp_1":"18:40:30",
            "image":(imgfile, open(imgfile, "rb"), "image/png"),
#            "faceImage":"",
            "aiid":"02",
            "jobid":"03",
            "event": (None, json.dumps({'tags': [4, 5, 6]}), 'application/json'),
            "description":"AI event",
            "reportedBy":"DeepAI",
            "eventlocation":(None, json.dumps({'rect': ['x', 'y', 'w', 'h']}), 'application/json'),
            "sourceid":"003",
            "site":"DeepAI",
            "properties":"N/A",
            "scenarios_properties":"ALERT",
            "status":"DETECTED"
           } ,
           boundary='----WebKitFormBoundarymbJlWA930MM4HpMp'
        )
        file = {imgfile}     
        try:
            #, headers={'Content-Type': multipart_data.content_type} ; boundary=----WebKitFormBoundarymbJlWA930MM4HpMp
            response = sess.post(AIAlertConfig.ADD_EVENT_POST_URL,data=multipart_data,headers={'Content-Type': multipart_data.content_type},cookies=r.cookies)
            print("Server url : "+ AIAlertConfig.ADD_EVENT_POST_URL)
            print(response.status_code)
            print(response.text)
        except Exception as e:
            print ("Exception in EventAlertSend  {0} ".format(e))


def AIEvent_Alert_CallBack():
    print("Got the callback of AIEvent_Alert")

if __name__ == '__main__':
    aievent_alert=AIEvent_Alert(AIEvent_Alert_CallBack)
    aievent_alert.EventAlertJsonSend("value-purpose-design.png")