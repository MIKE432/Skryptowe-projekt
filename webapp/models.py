from django.db import models

# Create your models here.
from webapp.tools import TrainingTypes, ExerciseTypes


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    nick = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.TextField(null=False)
    salt = models.TextField(null=False, blank=True)
    avatar = models.ImageField(null=True, blank=True, default=None)
    session_id = models.CharField(max_length=30, blank=True, default=None, unique=True, null=True)


class Training(models.Model):

    TRAINING_TYPES = [
        (TrainingTypes.AEROBIC, "Aerobic"),
        (TrainingTypes.STRENGTH, "Strength"),
        (TrainingTypes.STRETCHING, "Stretching"),
        (TrainingTypes.BALANCE, "Balance"),
        (TrainingTypes.RECOVERY, "Recovery"),
        (TrainingTypes.CIRCUIT, "Circuit"),
        (TrainingTypes.FUNCTIONAL, "Functional"),
        (TrainingTypes.HIIT, "HIIT"),
        (TrainingTypes.INTERVAL, "Interval"),
        (TrainingTypes.CARDIO, "Cardio"),
        (TrainingTypes.TABATA, "Tabata"),
        (TrainingTypes.SUPERSET, "Super Set"),
        (TrainingTypes.OTHER, "Other")
        ]

    training_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    about = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField()
    training_calories = models.IntegerField(default=0, blank=True)
    training_type = models.CharField(choices=TRAINING_TYPES, default=TrainingTypes.OTHER, max_length=50)


class Series(models.Model):
    series_id = models.AutoField(primary_key=True)
    iteration = models.IntegerField(default=1)
    rest_time = models.IntegerField(default=0)
    training_id = models.ForeignKey(Training, related_name="series", on_delete=models.CASCADE)


class Exercise(models.Model):

    EXERCISE_TYPES = [
        (ExerciseTypes.ABS, "Abs"),
        (ExerciseTypes.ARM, "Arm"),
        (ExerciseTypes.BACK, "Back"),
        (ExerciseTypes.CHEST, "Chest"),
        (ExerciseTypes.COOLDOWN, "Cool down"),
        (ExerciseTypes.LEG, "Leg"),
        (ExerciseTypes.SHOULDER, "Shoulder"),
        (ExerciseTypes.STRETCHING, "Stretching"),
        (ExerciseTypes.WARMUP, "Warm up"),
        (ExerciseTypes.OTHER, "Other")
        ]

    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=1000)
    number = models.IntegerField()
    yt_link = models.CharField(max_length=500)
    photo = models.ImageField()
    series_id = models.ForeignKey(Series, related_name="exercises", on_delete=models.CASCADE)
    exercise_type = models.CharField(choices=EXERCISE_TYPES, default=ExerciseTypes.OTHER, max_length=50)
    exercise_calories = models.IntegerField(default=0, blank=True)

