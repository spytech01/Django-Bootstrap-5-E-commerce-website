# Generated by Django 4.1.3 on 2022-11-11 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='m_photo',
        ),
    ]
