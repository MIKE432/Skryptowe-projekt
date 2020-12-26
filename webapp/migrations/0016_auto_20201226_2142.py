# Generated by Django 3.1.4 on 2020-12-26 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0015_auto_20201226_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='exercise_calories',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_type',
            field=models.CharField(choices=[('ABS', 'Abs'), ('ARM', 'Arm'), ('BACK', 'Back'), ('CHEST', 'Chest'), ('COOLDOWN', 'Cool down'), ('LEG', 'Leg'), ('SHOULDER', 'Shoulder'), ('STRETCHING', 'Stretching'), ('WARMUP', 'Warm up'), ('OTHER', 'Other')], default='OTHER', max_length=50),
        ),
        migrations.AddField(
            model_name='training',
            name='training_calories',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='training',
            name='training_type',
            field=models.CharField(choices=[('AEROBIC', 'Aerobic'), ('STRENGTH', 'Strength'), ('STRETCHING', 'Stretching'), ('BALANCE', 'Balance'), ('RECOVERY', 'Recovery'), ('CIRCUIT', 'Circuit'), ('FUNCTIONAL', 'Functional'), ('HIIT', 'HIIT'), ('INTERVAL', 'Interval'), ('CARDIO', 'Cardio'), ('TABATA', 'Tabata'), ('SUPERSET', 'Super Set'), ('OTHER', 'Other')], default='OTHER', max_length=50),
        ),
    ]
