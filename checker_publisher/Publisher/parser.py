#!/usr/bin/python3
from .models import Sended

def parse_twitter(resp):
    """
    Parses and save the twitter publication response
    """
    new_message = Sended()
    new_message.channel = 'twitter'
    new_message.content = resp['text']
    new_message.user_name = resp['user']['name']
    new_message.user_screen_name = resp['user']['screen_name']
    new_message.img_url = resp['user']['profile_image_url']
    new_message.checker_url = resp['entities']['media'][0]['media_url']
    new_message.save()
    return new_message.to_dict()

