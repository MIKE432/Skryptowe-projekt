from django.core.exceptions import ObjectDoesNotExist

from webapp.Errors import BadRequestException, NotFoundException
from webapp.models import Training
from webapp.serializers import TrainingSerializer, RawTrainingSerializer
from webapp.tools import perform_get


def get_training_by_args(**kwargs):
    training = perform_get(Training.objects.get, **kwargs)

    if training is None:
        return None

    serializer = TrainingSerializer(training)
    return serializer.data


def create_new_training(training):
    serializer = RawTrainingSerializer(data=training)

    if not serializer.is_valid():
        return None

    serializer.save()

    return serializer.data


def update_training(training_id, **kwargs):
    training = perform_get(Training.objects.get, training_id=training_id)

    if training is None:
        return None

    for k, v in kwargs.items():
        setattr(training, k, v)

    training.save(update_fields=kwargs.keys())

    return training
