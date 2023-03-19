# Generated by Django 3.2.3 on 2021-09-18 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Shipping'), (2, 'Billing')]),
        ),
    ]