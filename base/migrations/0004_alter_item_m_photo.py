# Generated by Django 4.1.3 on 2023-01-10 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_item_m_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='m_photo',
            field=models.ImageField(null=True, upload_to='photos/%Y/%m/%d'),
        ),
    ]
