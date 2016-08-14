
import json, requests, random, re
from pprint import pprint
from .models import reminders   
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import json
import urllib

import moment
from datetime import datetime
import time


def post_facebook_message(fbid, recevied_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAHZAyF2pZAlMBAAXAmutZAkKggoHzIZARtTFmUcLvsqUClJoZCvdUZCggsxBXyibjo1iIoNZBt0szKChpTJDukzb1pBrPNS53y9g0osjocxIWuitXA58VQuzhRGHXXR7tPpeXKIBTZCe5JRPTz4PttNee2ZC8x1N9yUdSUfoKf0wgQZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


all_reminders = reminders.objects.all()

for i in all_reminders:
    event_date = i.remindertime
    event_date = datetime.strptime(event_date)
    nowdate = datetime.now()
    senderid = i.receiverid
    if (event_date-nowdate).days == 1:
        if i.reminderalarm == False:
            reminder_message = "Upcoming event " + i.reminderdata + "on" + i.remindertime
            i.reminderalarm = True
            i.save()
            post_facebook_message(senderid, reminder_message)