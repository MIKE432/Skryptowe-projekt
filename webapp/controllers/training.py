from rest_framework import status
from rest_framework.response import Response

from webapp.Errors import *
from webapp.models import Training
from webapp.serializers import UserRawSerializer, TrainingSerializer


def get_training(request):
    serializer = UserRawSerializer(data=request.data)

    if not serializer.is_valid():
        raise BadRequestException("User with given nickname exists")

    serializer.save()
    serializer.data.pop('password')
    user = serializer.data
    del user['password']
    del user['salt']

    return Response(user, status.HTTP_201_CREATED)


def get_training_by_id(request, training_id):
    training = Training.objects.get(training_id=training_id)
    serializer = TrainingSerializer(training)
    return Response(serializer.data)
