from django.db import models

class Channel(models.Model):
    """
    stores channel Api credentials
    """
    name = models.CharField(max_length=100, default='ninguno')
    api_key = models.CharField(max_length=100)
    api_secret = models.CharField(max_length=100)
    token = models.CharField(max_length=100, blank=True, null=True)
    token_secret = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    def to_dict(self):
        return {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'token': self.token,
            'token_secret': self.token_secret,
            'email': self.email
        }

class Sended(models.Model):
    """
    Model of sended messages
    """
    channel = models.CharField(max_length=100, default='twitter')
    status_id = models.CharField(max_length=100, default='')
    user_name = models.CharField(max_length=100, default='')
    user_screen_name = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=300, default='')
    img_url = models.CharField(max_length=300, default='')
    checker_url = models.CharField(max_length=300, default='')
    date = models.CharField(max_length=300, default='')
    email = models.CharField(max_length=300, default='')

    def to_dict(self):
        """
        return dict repr
        """
        return {
            'channel': self.channel,
            'status_id': self.status_id,
            'user_name': self.user_name,
            'user_screen_name': self.user_screen_name,
            'content': self.content,
            'img_url': self.img_url,
            'checker_url': self.checker_url,
            'date': self.date,
            'email': self.email
        }
