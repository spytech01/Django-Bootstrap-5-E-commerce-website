# Generated by Django 4.1.3 on 2023-01-10 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_item_m_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='m_photo',
        ),
    ]
