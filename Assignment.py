import requests
import json
import MQSend
from Config import TEMPDICT


def TempAck(channel, delivery_tag, properties, body):
    channel.basic_ack(delivery_tag)
    type = properties.headers['type']
    uid = properties.headers['uid']
    if uid is None:
        print("empty channel")
    strB = str(body, encoding="utf-8")
    jsonFile = json.loads(strB)
    photoB = bytes('emtpy', 'utf-8')
    audioB = bytes('empty', 'utf-8')
    name = "empty"
    xuehao = "empty"
    if ('photo' in jsonFile):
        photo = jsonFile['photo']
        photoB = bytes(photo, "utf-8")
    if ('audio' in jsonFile):
        audio = jsonFile['audio']
        audioB = bytes(audio, "utf-8")
    if ('name' in jsonFile):
        name = jsonFile['name']
    if ('xuehao' in jsonFile):
        xuehao = jsonFile['xuehao']
    if type == "login":
        params = {
            'audio': audioB,
            'photo': photoB,
            'uid': uid
        }
        SimCheck0913(params, uid, type)
    if type == "register":
        params = {
            'audio': audioB,
            'photo': photoB,
            'uid': uid,
            'name': name,
            'xuehao': xuehao
        }
        Register(params, uid, type)
    if type == "registerFace":
        params = {
            'photo': photoB,
            'uid': uid,
            'name': name,
            'xuehao': xuehao
        }
        RegisterFace(params, uid, type)
    if type == "loginFace":
        params = {
            'photo': photoB,
            'uid': uid,
            'name': name,
            'xuehao': xuehao,
        }
        SimCheckFace(params, uid, type)
    if type == "loginVoice":
        global TEMDICT
        idList = TEMDICT[uid]["top_id"]
        simList = TEMPDICT[uid]["top_sim"]
        nameList = TEMPDICT[uid]["top_name"]
        params = {
            'idList': idList,
            'simList': simList,
            'nameList': nameList,
            'audio': audioB,
            'uid': uid,
        }
        SimCheckVoice(params, uid, type)
    print(1)


def SimCheck(params, uid, type):
    voice_check_url = 'http://127.0.0.1:8000/voiceprintcheck/simcheck'
    face_check_url = 'http://127.0.0.1:8001/facecheck/simcheck'
    headers = {}
    voice_check_res = requests.post(voice_check_url, data=params, headers=headers)
    face_check_res = requests.post(face_check_url, data=params, headers=headers)
    voice_back = json.loads(voice_check_res.text)["data"]
    face_back = json.loads(face_check_res.text)["data"]
    voice_best_id = voice_back["best_id"]
    face_best_id = face_back["best_id"]
    voice_sim = float(voice_back["best_sim"])
    face_sim = float(face_back["best_sim"])
    voice_name = voice_back["best_name"]
    face_name = face_back["best_name"]
    print(face_name, face_sim)
    if face_sim > 0.7:
        xuehao = face_best_id
        success = "yes"
        name = face_name
        print(name, xuehao)
        print(success)
    elif face_sim <= 0.7:
        xuehao = " "
        success = "no"
        name = " "
        print(success)
        print(type)
        print(xuehao)
        print(name)
    MQSend.send2MQLogin(uid, name, success, xuehao, type)


def SimCheckFace(params, uid, type):
    face_check_url = 'http://127.0.0.1:8001/facecheck/simcheckFace'
    headers = {}
    face_check_res = requests.post(face_check_url, data=params, headers=headers)
    face_back = json.loads(face_check_res.text)["data"]
    face_best_id = face_back["best_id"]
    face_sim = float(face_back["best_sim"])
    face_name = face_back["best_name"]
    print(face_name, face_sim)
    if face_sim > 0.7:
        xuehao = face_best_id
        success = "yes"
        name = face_name
        resultDict = face_back["resultDict"]
        global TEMPDICT
        TEMPDICT[str(uid)] = resultDict
        print(name, xuehao)
        print(success)
    elif face_sim <= 0.7:
        xuehao = " "
        success = "no"
        name = " "
        print(success)
        print(type)
        print(xuehao)
        print(name)

    MQSend.send2MQLogin(uid, name, success, xuehao, type)
    pass


def SimCheckVoice(params, uid, type):
    voice_identify_url = 'http://127.0.0.1:8000/voiceprintcheck/simcheckVoice'
    headers = {}
    voice_identify_res = requests.post(voice_identify_url, data=params, headers=headers)
    voice_back = json.loads(voice_identify_res.text)["data"]
    best_sim = voice_back["best_sim"]
    best_id = voice_back["best_id"]
    best_name = voice_back["best_name"]
    success = voice_back["success"]
    MQSend.send2MQLogin(uid, best_name, success, best_id, best_sim)
    del TEMPDICT[uid]


def Register(params, uid, type):
    voiceurl = 'http://127.0.0.1:8000/voiceprintcheck/register'
    faceurl = 'http://127.0.0.1:8001/facecheck/register'
    headers = {}
    voice_res = requests.post(voiceurl, data=params, headers=headers)
    face_res = requests.post(faceurl, data=params, headers=headers)
    voice_res1 = voice_res.text
    face_res1 = face_res.text
    voice_back = json.loads(voice_res1)["data"]
    print(voice_back)
    face_back = json.loads(face_res1)["data"]
    print(face_back)
    xuehao = params["xuehao"]
    name = params["name"]
    success = "yes"
    if (voice_back != "success") or (face_back != "success"):
           success = "no"
    print(success)
    MQSend.send2MQRegister(uid, xuehao, success, name, type)


def RegisterFace(params, uid, type):
    faceurl = 'http://127.0.0.1:8001/facecheck/registerFace'
    headers = {}
    face_res = requests.post(faceurl, data=params, headers=headers)
    face_res1 = face_res.text
    face_back = json.loads(face_res1)["data"]
    print(face_back)
    xuehao = params["xuehao"]
    name = params["name"]
    success = "yes"
    if face_back != "success":
           success = "no"
    print(success)
    MQSend.send2MQRegister(uid, xuehao, success, name, type)


def SimCheck0913(params, uid, type):
    face_check_url = 'http://127.0.0.1:8001/facecheck/simcheck'
    headers = {}
    face_check_res = requests.post(face_check_url, data=params, headers=headers)
    face_back = json.loads(face_check_res.text)["data"]
    face_best_id = face_back["best_id"]
    face_sim = float(face_back["best_sim"])
    face_name = face_back["best_name"]
    if face_sim > 0.7:
        xuehao = face_best_id
        name = face_name
        print(name, xuehao)
        success = VoiceIdentifier(name, params)
        print(success)
    elif face_sim <= 0.7:
        xuehao = " "
        success = "no"
        name = " "
        print(success)
        print("fail")
        print(type)
        print(xuehao)
        print(name)
    MQSend.send2MQLogin(uid, name, success, xuehao, type)


def VoiceIdentifier(name, params):
    voice_identify_url = 'http://127.0.0.1:8000/voiceprintcheck/identify'
    headers = {}
    params['name'] = name
    voice_identify_res = requests.post(voice_identify_url, data=params, headers=headers)
    voice_back = json.loads(voice_identify_res.text)["data"]
    success = voice_back["success"]
    return success