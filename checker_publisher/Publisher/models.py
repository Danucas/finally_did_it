from django.db import models

# Create your models here.

class User(models.Model):
    """
    User info, pass, email and API key
    """
    api_key = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    token = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=5, blank=True, null=True)
    def __str__(self):
        return self.email

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
        }


class Project(models.Model):
    """
    stores projects ids and names
    """
    project_id = models.CharField(max_length=4)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.project_id + ' ' + self.name


class Channel(models.Model):
    """
    stores channel Api credentials
    """
    name = models.CharField(max_length=100, default='ninguno')
    api_key = models.CharField(max_length=100)
    api_secret = models.CharField(max_length=100)
    token = models.CharField(max_length=100, blank=True, null=True)
    token_secret = models.CharField(max_length=100, blank=True, null=True)

    def to_dict(self):
        return {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'token': self.token,
            'token_secret': self.token_secret
        }

class Sended(models.Model):
    """
    Model of sended messages
    """
    channel = models.CharField(max_length=100)
    status_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_screen_name = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    img_url = models.CharField(max_length=300)
    checker_url = models.CharField(max_length=300)
    date = models.CharField(max_length=300)

    def to_dict(self):
        """
        return dict repr
        """
        return {
            'channel': self.channel,
            'status_id': self.status_id,
            'user_name': self.user_name,
            'user_screen_name': self.user.user_screen_name,
            'content': self.content,
            'img_url': self.img_url,
            'checker_url': self.checker_url,
            'date': self.date
        }