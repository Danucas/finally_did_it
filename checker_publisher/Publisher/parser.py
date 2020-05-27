#!/usr/bin/python3
from .models import Sended

def parse_twitter(resp, email):
    """
    Parses and save the twitter publication response
    """
    new_message = Sended()
    new_message.channel = 'twitter'
    new_message.content = ' '.join(resp['text'].split(' ')[:-1])
    new_message.user_name = resp['user']['name']
    new_message.user_screen_name = resp['user']['screen_name']
    new_message.img_url = resp['user']['profile_image_url']
    new_message.checker_url = resp['entities']['media'][0]['media_url']
    new_message.status_id = resp['id']
    new_message.date = ' '.join(resp['created_at'].split(' ')[:3])
    new_message.email = email
    new_message.save()
    return new_message.to_dict()

