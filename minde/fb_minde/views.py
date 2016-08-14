
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

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAAHZAyF2pZAlMBAAXAmutZAkKggoHzIZARtTFmUcLvsqUClJoZCvdUZCggsxBXyibjo1iIoNZBt0szKChpTJDukzb1pBrPNS53y9g0osjocxIWuitXA58VQuzhRGHXXR7tPpeXKIBTZCe5JRPTz4PttNee2ZC8x1N9yUdSUfoKf0wgQZDZD"
VERIFY_TOKEN = "2318934571"

jokes = { 'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""", 
                     """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""], 
         'fat':      ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""", 
                      """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """], 
         'dumb': ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""", 
                  """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] }


# Helper function
def post_facebook_message(fbid, recevied_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAHZAyF2pZAlMBAAXAmutZAkKggoHzIZARtTFmUcLvsqUClJoZCvdUZCggsxBXyibjo1iIoNZBt0szKChpTJDukzb1pBrPNS53y9g0osjocxIWuitXA58VQuzhRGHXXR7tPpeXKIBTZCe5JRPTz4PttNee2ZC8x1N9yUdSUfoKf0wgQZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


# Post function to handle Facebook messages
def short_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyB0N1UrT-OxThltr9Lr1bb1IeCuYma-rro'
    params = json.dumps({'longUrl': url})
    response = requests.post(post_url,params,headers={'Content-Type': 'application/json'})
    response1=json.loads(response.text)
    return response1['id']
# Create your views here.
class mindeview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token') == VERIFY_TOKEN:
            return HttpResponse(self.request.GET.get('hub.challenge'))
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)



    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    # pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 

                    # if images or extra achievements will be added in attachmetns 
                    try:
                        senderid = message['sender']['id']
                        if senderid != 860649504016574:
                            pprint(message)
                            try:
                                text = message['message']['text']
                                # post_facebook_message(senderid, message['message']['text'])
                            except KeyError:
                                pass
                    except KeyError:
                        pass

                    if "attachments" in message['message']:
                        if message['message']['attachments'][0]['type'] == "image":
                            print message['message']['attachments'][0]['payload']['url']

                            image_url = message['message']['attachments'][0]['payload']['url']
                            print image_url
                            # bitapi = requests.get('https://api-ssl.bitly.com/v3/shorten?access_token=7b695710814d6c5ae58e8d5db6bd4c0ba7be2085&longUrl='+image_url)
                            # biturl = json.loads(bitapi.text)
                            # short_url= biturl['data']['url']
                            short_img_url = short_url(image_url)
                            correct_url = 'http://api.havenondemand.com/1/api/async/ocrdocument/v1?apikey=d8023014-ab1d-4831-9b2f-7b9946932405&url='+short_img_url
                            print correct_url
                            ptext= requests.get(correct_url)
                            job=json.loads(ptext.text)
                            print job
                            data= requests.get('http://api.havenondemand.com/1/job/result/%s?apikey=d8023014-ab1d-4831-9b2f-7b9946932405' %job['jobID'])
                            dataload=json.loads(data.text)
                            print dataload
                            try:
                                impdata=((((dataload['actions'])[0]['result'])['text_block'])[0]['text'])
                            except KeyError:
                                pass

                            text1=requests.get('http://api.meaningcloud.com/topics-2.0?key=26f841b83b15255990e9a1cfed9a47a9&of=json&lang=en&ilang=en&txt='+impdata+'&tt=a&uw=y')
                            textp=json.loads(text1.text)

                            print textp['time_expression_list']


                            
                            for t in textp['time_expression_list']:
                                if t['precision'] == "day" or t['precision'] == "weekday":
                                   dates = t['actual_time']
                                   tim = "08:33:54.227806"
                                   rtime = dates + rtime
                                   # rtime = datetime.strptime(rtime, "%Y-%m-%d %H:%M:%S.%f")

                                else:
                                    dates = datetime.now()
                                    rtime = dates.strftime("%Y-%m-%d")
                                    time_poster = t['actual_time']
                                    time_poster = time_poster.split(" ")
                                    rtime = rtime + " " + time_poster[0]
                                    # rtime = datetime.strptime(rtime, "%Y-%m-%d %H:%M:%S.%f")
                            
                            try:
                                reminderdata = textp['relation_list'][0]['form']
                            except KeyError:
                                reminderdata = " No information"


                            k = reminders.objects.create(receiverid=senderid, remindertime=rtime, reminder=reminderdata)


                        
        return HttpResponse()    


def send_reminders(self):
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
            

