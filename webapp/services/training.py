from django.core.exceptions import ObjectDoesNotExist

from webapp.Errors import BadRequestException, NotFoundException
from webapp.models import Training
from webapp.serializers import TrainingSerializer
from webapp.tools import perform_get


def get_training_by_args(**kwargs):
    training = perform_get(Training.objects.get, **kwargs)

    if training is None:
        raise NotFoundException("There is no training with given id")

    serializer = TrainingSerializer(training)
    return serializer.data


def create_new_training(training):
    serializer = TrainingSerializer(data=training)

    if not serializer.is_valid():
        raise BadRequestException(serializer.errors)

    serializer.save()

    return serializer.data
