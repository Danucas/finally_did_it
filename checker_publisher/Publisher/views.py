from django.shortcuts import render
from django.http.response import HttpResponse
from .models import User, Project, Channel, Sended
import requests
import json
import uuid
import base64
from .twitter_api import Tapi
from .media_upload import GifTweet
from .parser import parse_twitter

# Create your views here.


def dashboard(request):
    """
    Form to store the media setup
    API keys etc...
    """
    print(request)
    res = render(request, 'dashboard.html', {'id': uuid.uuid4()})
    return res


def save_user(request):
    """
    save the user
    """
    api_key = request.GET.get('api_key')
    email = request.GET.get('email')
    passwd = request.GET.get('pass')
    new_user = User()
    new_user.api_key = api_key
    new_user.email = email
    new_user.password = passwd
    new_user.save()
    return check_user(request)


def check_user(request):
    """
    check if an user exists
    """
    users = User.objects.all()
    # print('Users\t', users, len(users))
    content = str(users)
    resp = HttpResponse()
    if len(users) == 0:
        content = 'Not found'
        resp.status_code = 404
        resp.content = content
        return resp
    else:    
        user = users[0]
        print(user.to_dict())
        if user.token != None:
            print('token exists')
            url = 'https://intranet.hbtn.io/users/me.json?auth_token=' + user.token
            resp = requests.get(url)
            if resp.status_code == 200:
                return HttpResponse(json.dumps(user.to_dict()), content_type='application/json')
            else:
                print('request new token')
                user.token = None
                user.save()
                check_user(request)
        url = 'https://intranet.hbtn.io/users/auth_token.json'
        data = {
            'api_key': user.api_key,
            'email': user.email,
            'password': user.password,
            'scope': 'checker'
        }
        header = {'Content-Type': 'application/json'}
        user_info = requests.post(url, json=data, headers=header)
        if user_info.status_code == 200:
            user.token = user_info.json()['auth_token']
            user.username = user_info.json()['full_name']
            user.user_id = user_info.json()['user_id']
            user.save()
            return HttpResponse(json.dumps(user.to_dict()), content_type="application/json")
        else:
            user.delete()
            print(user_info.status_code, user_info.reason)
            resp = HttpResponse()
            resp.status_code = 401
            return resp


def search_project(request):
    """
    Handles project request
    """
    id = request.GET.get('project_id')
    user = User.objects.all()
    if (len(user) == 0):
        return HttpResponse()
    else:
        user = user[0]
    url = 'https://intranet.hbtn.io/projects/' + id + '.json'
    param = {'auth_token': user.token}
    resp = requests.get(url, params=param, headers={'Content-Type': 'application/json'})
    if resp.status_code == 200:
        project = Project()
        project.project_id = id
        project.name = resp.json()['name']
        project.save()
        js = resp.json()
        js['p'] = resp.json()['name']
        html = render(request, 'project.html', js)
        return html
    else:
        print(resp.status_code, resp.reason)
        return HttpResponse()


def check_task(request):
    """
    ask for a new correction
    """
    user = User.objects.all()
    if (len(user) == 0):
        return HttpResponse()
    else:
        user = user[0]
    id = request.GET.get('task')
    url = 'https://intranet.hbtn.io/tasks/' + id + '/start_correction.json?auth_token='+ user.token
    param = {}
    resp = requests.post(url, data=param, headers={'Content-Type': 'application/json'})
    if resp.status_code == 200:
        while True:
            uri = 'https://intranet.hbtn.io/correction_requests/' +\
                str(resp.json()['id']) + '.json?auth_token=' + user.token
            corr = requests.get(uri, headers={'Content-Type': 'application/json'})
            if (corr.json()['status'] == 'Sent'):
                pass
            elif (corr.json()['status'] == 'Done'):
                # print(corr.json())
                html = render(request, 'checker.html', corr.json()['result_display'])
                print(html)
                return html
            else:
                print('error')
                break
    return HttpResponse(json.dumps(resp.json()), content_type='application/json')

def send_twitter(filename, message, twitter):
    """
    Send the image via twitter Using Tapi
    """
    # cons_key = "rkmNCkTPy1W5xPaKYiRevP8V6"
    # cons_sec = "52sL2OeMwURDWNyh39vjfJFm2UKTYpSlJwOAcis5CTloftDa0j"
    # acc_tok = "1144866141090799616-3v6RJ1rXrdjPqL5ctJQ5sqP8rlVHDd"
    # acc_tok_sec = "3ldeSHcohBnt87cwEYUKp9O9Rxv2liUge5q9guJS23Iav"
    api = Tapi(twitter.api_key,
                twitter.api_secret,
                twitter.token,
                twitter.token_secret)
    # Accessing Twitter
    # Creating API handler instance
    
    uploader = GifTweet(filename, api)
    uploader.upload_init('image/png')
    uploader.upload_append()
    uploader.upload_finish()
    uploader.check_status()
    # Get the message
    
    return uploader.post(message).json()
    # return 'done'
 


def send_image(request):
    """
    Send image to channels
    """
    channels = ''.join(request.POST.get('channels')).split(',')
    print('channels', channels)
    if channels[0] == '':
        return HttpResponse(status=305)
    # saving image in disk
    image = bytes(request.POST.get('image').split(',')[1], 'utf-8')
    image = base64.decodebytes(image)
    with open('test.png', 'wb') as fil:
        fil.write(image)
    filename = 'test.png'
    message = request.POST.get('content')
    resp = []
    for channel in channels:
        media = Channel.objects.filter(name=channel)
        if len(media) == 0:
            return HttpResponse(json.dumps({'media': channel}), status=404, content_type='application/json')
        else:
            pass
    for channel in channels:
        media = Channel.objects.filter(name=channel)
        if channel == 'twitter':
            resp.append(send_twitter(filename, message, media[0]))
        if channel == 'slack':
            pass
    print(resp)
    resp = parse_twitter(resp[0])
    template = render(request, 'sended_messages.html', {'messages': resp})
    return HttpResponse()

def save_channel(request):
    """
    save the channel model
    """
    print(request.GET)
    channel = Channel.objects.filter(name=request.GET.get('channel'))
    if len(channel) == 0:
        channel = Channel()
    else:
        channel = channel[0]
    channel.name = request.GET.get('channel')
    channel.api_key = request.GET.get('api_key')
    channel.api_secret = request.GET.get('api_secret')
    channel.token = request.GET.get('token')
    channel.token_secret = request.GET.get('token_secret')
    channel.save()
    print(channel)

    return HttpResponse()

def check_channel(request):
    """
    Chek if a channel already exists return the dict
    """
    name = request.GET.get('channel')
    channel = Channel.objects.filter(name=name)
    if len(channel) == 0:
        return HttpResponse(status=404)
    return HttpResponse(json.dumps(channel[0].to_dict()), content_type='application/json')