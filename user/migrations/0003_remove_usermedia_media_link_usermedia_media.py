# Generated by Django 4.2.5 on 2023-10-12 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_user_id_usermedia_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermedia',
            name='media_link',
        ),
        migrations.AddField(
            model_name='usermedia',
            name='media',
            field=models.ImageField(default='', unique=True, upload_to='user_images/'),
            preserve_default=False,
        ),
    ]
