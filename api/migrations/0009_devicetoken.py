# Generated by Django 4.1.3 on 2023-08-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_questioncategory_question_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.UUIDField()),
                ('token', models.CharField(default='', max_length=1000)),
            ],
        ),
    ]
