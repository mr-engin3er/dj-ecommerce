# Generated by Django 3.1.5 on 2021-02-15 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='address',
            name='default_address',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='order.city'),
        ),
        migrations.AlterField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='order.state'),
        ),
    ]