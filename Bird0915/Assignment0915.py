import requests
import json
from Bird0915.MQSend0915 import send2Server



def Assign(channel, delivery_tag, properties, body):
    channel.basic_ack(delivery_tag)
    type = properties.headers['type']
    uid = properties.headers['uid']
    if uid is None:
        print("empty channel")
    strB = str(body, encoding="utf-8")
    jsonFile = json.loads(strB)
    if 'url' in jsonFile:
        url = jsonFile['url']
    if type == "hls":
        params = {
            'url': url
        }
        birdCheck(params, uid, type)
    print(1)


def birdCheck(params, uid, type):
    success = "no"
    try:
        bird_check_url = 'http://127.0.0.1:8002/bird/birdCheck0915'
        headers = {}
        bird_check_res = requests.post(bird_check_url, data=params, headers=headers)
        jsonRes = json.loads(bird_check_res.text)
        url = jsonRes["url"]
        bird_location = jsonRes["data"]
        suceess = "yes"
    except Exception as e:
        pass
    send2Server(uid, suceess, url, bird_location, type)
