# Generated by Django 4.1.3 on 2023-06-29 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image_url',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
