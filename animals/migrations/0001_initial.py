# Generated by Django 4.2.5 on 2023-09-17 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
                ('breed', models.CharField(max_length=255)),
                ('availability', models.BooleanField()),
                ('description', models.TextField()),
                ('healthy', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('animal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animals.animal')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_link', models.CharField(max_length=255)),
                ('main', models.BooleanField()),
                ('animal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animals.animal')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='sex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animals.sex'),
        ),
    ]
