# Generated by Django 4.1.3 on 2023-02-01 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_payment_order_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='amoutn',
            new_name='amount',
        ),
    ]
