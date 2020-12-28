import hashlib

from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import User, Training, Series, Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class SeriesSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Series
        fields = "__all__"


class TrainingSerializer(serializers.ModelSerializer):
    series = SeriesSerializer(many=True)

    class Meta:
        model = Training
        fields = ['series', 'name', 'about', 'is_public', 'training_calories', 'training_type']

    # def create(self, validated_data):
    #     series = validated_data.pop('series')
    #     user = User.objects.get(pk=6)
    #     new_training = Training.objects.create(created_by=user, **validated_data)
    #     for _series in series:
    #         exercises = _series.pop('exercises')
    #         print("exer", exercises)
    #         new_series = Series.objects.create(training_id=new_training, **_series)
    #         for exercise in exercises:
    #             Exercise.objects.create(series_id=new_series, **exercise)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "nick", "name", "surname", "avatar"]


class UserRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        salt = get_random_string(length=15)
        password_and_salt = validated_data.pop('password') + salt
        hashed_password_and_salt = hashlib.sha256(password_and_salt.encode(encoding="utf-8")).hexdigest()
        user = User.objects.create(**validated_data, password=hashed_password_and_salt, salt=salt)
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nick', 'password']


class TrainingListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Training
        fields = "__all__"


class RawTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ['training_id', 'name', 'about', 'is_public', 'training_calories', 'training_type', 'created_by']


class RawSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['series_id', 'iteration', 'rest_time', 'training_id']


class RawExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['name', 'about', 'number', 'yt_link', 'photo', 'series_id', 'exercise_type', 'exercise_calories']

