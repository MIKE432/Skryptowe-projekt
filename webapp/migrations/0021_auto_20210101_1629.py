# Generated by Django 3.1.4 on 2021-01-01 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_auto_20210101_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='yt_link',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
