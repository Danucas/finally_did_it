# Generated by Django 3.0.5 on 2020-05-23 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Publisher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]