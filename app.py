
import sys
import json
import requests
import random
from flask import Flask, request
from urllib.request import urlopen

app = Flask(__name__)
VERIFY_TOKEN = 'ub7342tGB34BSDHHDFG'
PAGE_ACCESS_TOKEN ='EAAOmobUVC34BAGc151jhHOmdwNYVWzXRfNAGtq7BlcBW5ohZCKW1kcH4Pou0u1ZBhTXYwZC9qHsTMdQ7uKZAHEyLoXZBRZAIzkrPyolAT3EkJXlVN8hl4FZAesL9APm7ONK4lbXFxl2OLOee55wBPULZBh957YlYBK4YYQnwYnIKLTBxaApTpu8ocdv0xDvsgOTtF9bMFPQxIQZDZD'

@app.route('/', methods=['GET'])
def test():
    return "Hello world"
@app.route('/webhook', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/webhook', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":   # make sure this is a page subscription

        for entry in data.get("entry"):
            for messaging_event in entry.get("messaging"):
                sender_id = messaging_event["sender"]["id"]

                if messaging_event.get("message"):
                    handleMessage(sender_id, messaging_event.get("message") )
                    log("postback")
                    log(messaging_event.get("message"))
                elif messaging_event.get("postback"):
                    handlePostback(sender_id, messaging_event.get("postback"))
                    log("postback")
                    log(messaging_event.get("postback"))
                else:    # uknown messaging_event
                    log("Webhook received unknown messaging_event:")

    return "ok", 200
def handlePostback(sender_id, received_postback):
    payload = str(received_postback.get("payload"))
    if payload == "covid":
        rq = callApicovid("vn")
        response = {
            "text": f'số ca mắc là {str(rq.get("cases"))}  số người tử vong là: {str(rq.get("deaths")) } số người hồi phục là: {str(rq.get("recovered"))}',
        }
    elif payload == "tintuc":
        log("payload == tintuc")
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Is this the right picture?",
                        "subtitle": "Tap a button to answer.",
                        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0wvj2caokPnNWS6WOvcxabzYzGuCkFTWEyA&usqp=CAU",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "VN Express",
                                "payload": "vnexpress",
                            },
                            {
                                "type": "postback",
                                "title": "Kenh14",
                                "payload": "kenh14",
                            },
                        ],
                    }]
                }
            }
        }
    elif payload == "vnexpress":
        log("payload == vnexpress")
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Is this the right picture?",
                        "subtitle": "Tap a button to answer.",
                        "image_url": "https://s1cdn.vnecdn.net/vnexpress/restruct/i/v589/logo_default.jpg",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Sức khỏe",
                                "payload": "vnexpressSucKhoe",
                            },
                            {
                                "type": "postback",
                                "title": "Giáo dục",
                                "payload": "vnexpressGiaoDuc",
                            },
                            {
                                "type": "postback",
                                "title": "Pháp luật",
                                "payload": "vnexpressPhapLuat",
                            }
                        ],
                    }]
                }
            }
        }
    elif payload == "kenh14":
        log("payload == kenh14")
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Is this the right picture?",
                        "subtitle": "Tap a button to answer.",
                        "image_url": "http://rubee.com.vn/admin/webroot/upload/image//images/tin-tuc/kenh14-logo-2.png",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Âm nhạc",
                                "payload": "Kenh14Musik",
                            },
                            {
                                "type": "postback",
                                "title": "Thế giới",
                                "payload": "kenh14TheGioi",
                            },
                            {
                                "type": "postback",
                                "title": "Học đường",
                                "payload": "kenh14HocDuong",
                            }
                        ],
                    }]
                }
            }
        }
    elif payload == "thugian":
        log("payload == thugian")
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Is this the right picture?",
                        "subtitle": "Tap a button to answer.",
                        "image_url": "https://file.hstatic.net/200000312633/file/cach_thu_gian_dau_oc_truoc_khi_ngu_se_cho_ban_mot_giac_ngu_sau_1_1c6649f49edb46d2afd8bf64c2528f43.jpg",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "ảnh chó",
                                "payload": "anhcho",
                            },
                            {
                                "type": "postback",
                                "title": "thông tin thú vị về mèo",
                                "payload": "thongtinmeo",
                            },
                            {
                                "type": "postback",
                                "title": "ảnh meme",
                                "payload": "anhmeme",
                            }
                        ],
                    }]
                }
            }
        }
    elif payload == "anhcho":
        rq = requests.get('https://dog.ceo/api/breeds/image/random').json()
        response = {

            "attachment": {
                "type": "image",
                "payload": {
                    "url": rq['message'],
                    "is_reusable": True
                }

            }
        }
    elif payload == "anhmeme":
        rq = requests.get('https://api.imgflip.com/get_memes').json()
        arrMemes=rq['data']['memes']
        response = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": arrMemes[random.randrange(0, len(arrMemes), 1)]['url'],
                    "is_reusable": True
                }

            }
        }
    elif payload == "thongtinmeo":
        rq = requests.get('https://catfact.ninja/fact').json()
        response = {
            "text": rq['fact'],
        }
    elif payload == "vnexpressSucKhoe":
        rq = callApiCrawl("vnexpressSucKhoe")
        for x in rq[0:5]:
            response = {
                "text": x,
            }
            callSendAPI(sender_id, response)
    elif payload == "vnexpressGiaoDuc":
        rq = callApiCrawl("vnexpressGiaoDuc")
        for x in rq[0:5]:
            response = {
                "text": x,
            }
            callSendAPI(sender_id, response)
    elif payload == "vnexpressPhapLuat":
        rq = callApiCrawl("vnexpressPhapLuat")
        for x in rq[0:5]:
            response = {
                "text": x,
            }
            callSendAPI(sender_id, response)
    elif payload == "kenh14TheGioi":
        rq = callApiCrawl("kenh14TheGioi")
        for x in rq[0:5]:
            response = {
                "text": "https://kenh14.vn/"+x,
            }
            callSendAPI(sender_id, response)
    elif payload == "kenh14HocDuong":
        rq = callApiCrawl("kenh14HocDuong")
        for x in rq[0:5]:
            response = {
                "text": "https://kenh14.vn/"+x,
            }
            callSendAPI(sender_id, response)
    elif payload == "kenh14Musik":
        rq = callApiCrawl("kenh14Musik")
        for x in rq[0:5]:
            response = {
                "text": "https://kenh14.vn"+x,
            }
            callSendAPI(sender_id, response)
    else:
        response={
            "text": "",
        }
    callSendAPI(sender_id, response)
def callApiCrawl(parameter):
    result = requests.get('https://api-crawl.herokuapp.com/' + parameter).json()
    # log(result)
    return result
def handleMessage(sender_id, received_message):
    if received_message.get("text"):
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Is this the right picture?",
                        "subtitle": "Tap a button to answer.",
                        "image_url": "https://cdn.thuvienphapluat.vn/tintuc/uploads/image/2021/09/09/nCoV10.jpg",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "covid-19",
                                "payload": "covid",
                            },
                            {
                                "type": "postback",
                                "title": "Tin tức",
                                "payload": "tintuc",
                            },
                            {
                                "type": "postback",
                                "title": "Thư giãn",
                                "payload": "thugian",
                            },
                        ],
                    }]
                }
            }
        }
        callSendAPI(sender_id, response)

def callSendAPI(sender_id, request_body):
    log("111111111111111")
    log(request_body)

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": request_body

    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def callApicovid(country):
    result = requests.get('https://corona.lmao.ninja/v2/countries/' + country).json()
    # log(result)
    return result

def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)
    sys.stdout.flush()