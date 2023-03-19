# Generated by Django 3.2.3 on 2021-09-18 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.FloatField()),
                ('discounted_price', models.FloatField(blank=True, null=True)),
                ('size', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], max_length=2)),
                ('category', models.CharField(choices=[('S', 'Shirts'), ('SW', 'Sports wear'), ('C', 'Casuals'), ('OW', 'Outwear'), ('WW', 'Winter Wear')], max_length=2)),
                ('label', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
