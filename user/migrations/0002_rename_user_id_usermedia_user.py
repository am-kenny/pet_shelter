# Generated by Django 4.2.5 on 2023-09-17 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermedia',
            old_name='user_id',
            new_name='user',
        ),
    ]
