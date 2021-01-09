from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from webapp.Errors import BadRequestException, NotFoundException
from webapp.models import Training
from webapp.serializers import TrainingSerializer, RawTrainingSerializer, TrainingListSerializer
from webapp.services.user import get_user_by_args
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

    if 'training_id' in kwargs:
        del kwargs['training_id']

    if training is None:
        return None

    for k, v in kwargs.items():
        setattr(training, k, v)

    training.save(update_fields=kwargs.keys())

    return training


def get_all_trainings_by_session_id(session_id=None, **kwargs):
    user = get_user_by_args(session_id=session_id)

    if session_id is None or user is None:
        trainings = Training.objects.all().filter(is_public=True)

        return TrainingListSerializer(filter_trainings_by_args(trainings, **kwargs), many=True).data

    trainings = Training.objects.all().filter(Q(is_public=True) | Q(created_by=user['user_id']))
    filtered_trainings = filter_trainings_by_args(trainings, **kwargs)

    if kwargs['training_type'] == '':
        return TrainingListSerializer(filtered_trainings, many=True).data
    else:
        return TrainingListSerializer(filtered_trainings.filter(Q(training_type=kwargs['training_type'])),
                                      many=True).data


def delete_training(training_id):
    training = perform_get(Training.objects.get, training_id=training_id)

    if training is None:
        return None

    training.delete()

    return True


def filter_trainings_by_args(trainings, **kwargs):
    return trainings.filter(Q(training_calories__lte=kwargs['training_calories_max']) &
                            Q(training_calories__gte=kwargs['training_calories_min']) &
                            Q(name__contains=kwargs['training_name']))


def get_user_trainings_by_id(session_id, user_id):
    user = get_user_by_args(session_id=session_id)

    if user is None:
        trainings = Training.objects.all().filter(created_by=user_id, is_public=True)
        return TrainingListSerializer(trainings, many=True).data

    if user['user_id'] == user_id:
        trainings = Training.objects.all().filter(created_by=user_id)

        return TrainingListSerializer(trainings, many=True).data
