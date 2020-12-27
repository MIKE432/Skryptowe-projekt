from rest_framework import status
from rest_framework.response import Response

from webapp.Errors import NotFoundException
from webapp.services.training import create_new_training, get_training_by_args


def get_training_by_id(request, training_id):
    training = get_training_by_args(training_id=training_id)

    return Response(training, status.HTTP_200_OK)


def create_training(request):
    training = create_new_training(request.data)

    return Response({"training": None}, status.HTTP_200_OK)
