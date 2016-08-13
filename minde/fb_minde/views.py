
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

    # Post function to handle Facebook messages
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
                        sender = message['sender']['id']
                        if sender != 860649504016574:
                            pprint(message)
                        post_facebook_message(sender, message['message']['text'])
                    except KeyError:
                        pass

                    if "attachments" in message['message']:
                        if message['message']['attachments'][0]['type'] == "image":
                            print message['message']['attachments'][0]['payload']['url']

                            image_url = message['message']['attachments'][0]['payload']['url']


                        
        return HttpResponse()    