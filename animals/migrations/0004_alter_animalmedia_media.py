# Generated by Django 4.2.5 on 2023-10-11 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0003_rename_main_animalmedia_is_main_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalmedia',
            name='media',
            field=models.ImageField(unique=True, upload_to='animal_images/'),
        ),
    ]
