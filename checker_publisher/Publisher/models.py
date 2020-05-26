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
    api_key = models.CharField(max_length=100)
    api_secret = models.CharField(max_length=100)
    token = models.CharField(max_length=100, blank=True, null=True)