# Generated by Django 3.1.4 on 2020-12-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_user_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='session_id',
            field=models.CharField(blank=True, default=None, max_length=30),
        ),
    ]