
import sys
import json
import requests

from flask import Flask, request
from urllib.request import urlopen

app = Flask(__name__)
VERIFY_TOKEN = 'ub7342tGB34BSDHHDFG'
PAGE_ACCESS_TOKEN = 'EAAOmobUVC34BANSAhNymEamJwSKQY2vLUqMNnp108gnbKhZAz8LZCe1SXqP5WBbs5upnjU9nzEMjJDejW5zZAtFaZA8OXdYp2wZAbkZBRaxf8LwsiJZAPv03XkSzV5zOYc7vMMyZALeV7XJZBisw8lSYX0CQowQ7EZBHCfrE42zZBCYPf2GMX2yu1vZCYDZB8mdzbcZBlTdiomaO2zoAZDZD'
ID_CITY=[]
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
            "text": f'số ca mắc là {str(rq.get("cases"))}  số người tử vong là: {str(rq.get("deaths")) }số người hồi phục là: {str(rq.get("recovered"))}',
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
                        "image_url": "https://static.ybox.vn/2020/4/3/1586938466864-1582303297391-1574763681287-1570840773007-Thi%E1%BA%BFt%20k%E1%BA%BF%20kh%C3%B4ng%20t%C3%AAn.png",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "sport",
                                "payload": "kenk14Sport",
                            },
                            {
                                "type": "postback",
                                "title": "thegioi",
                                "payload": "kenh14TheGioi",
                            },
                            {
                                "type": "postback",
                                "title": "hocduong",
                                "payload": "kenh14HocDuong",
                            }

                        ],
                    }]
                }
            }
        }
    elif payload == "kenk14Sport":
        rq = callApiCrawl("Kenh14Sport")
        for x in rq:
            response = {
                "text": "https://kenh14.vn/"+x,
            }
            callSendAPI(sender_id, response)
    else:
        response={
            "text": "https://kenh14.vn/",
        }
    callSendAPI(sender_id, response)
def callApiCrawl(parameter):
    result = requests.get('https://api-crawl.herokuapp.com/' + parameter).json()
    # log(result)
    return result
def handleMessage(sender_id, received_message):
    if received_message.get("text"):
        # message_text = received_message.get("text").upper()
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
                                "title": "vnexpress",
                                "payload": "vnexpress",
                            },
                            {
                                "type": "postback",
                                "title": "kenh14",
                                "payload": "kenh14",
                            }

                        ],
                    }]
                }
            }
        }
    elif  received_message.get("attachments"):
        attachment_url = received_message["attachments"][0]["payload"].get("url")
        url = 'https://emoplay.herokuapp.com'
        with urlopen(attachment_url) as file:
            content = file.read()
        emoplay = requests.post(url, files={'image': content}).json()
        response = {
            "text": emoplay.get("result")
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

    r = requests.post("https://graph.facebook.com/v4.0/me/messages", params=params, headers=headers, data=data)
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

