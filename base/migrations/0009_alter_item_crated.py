# Generated by Django 4.1.3 on 2023-01-31 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_item_crated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='crated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
