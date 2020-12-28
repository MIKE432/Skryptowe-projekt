from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from webapp.Errors import NotFoundException, BadRequestException, UnauthorizedException, InternalServerException
from webapp.models import Exercise
from webapp.services.exercise import create_new_exercise
from webapp.services.series import create_new_series
from webapp.services.training import create_new_training, get_training_by_args, update_training
from webapp.services.user import get_user_by_args


def get_training_by_id(request, training_id):
    training = get_training_by_args(training_id=training_id)

    if training is None:
        raise NotFoundException("There is no training with given id")

    return Response(training, status.HTTP_200_OK)


@transaction.atomic
def create_training(request):
    request_body = request.data

    if 'session_id' not in request.query_params:
        raise BadRequestException("No session id provided")

    session_id = request.query_params['session_id']

    training = request_body
    series = training.pop('series')
    user = get_user_by_args(session_id=session_id)

    if user is None:
        raise UnauthorizedException(f'invalid session id: {session_id}')

    training['created_by'] = user['user_id']

    created_training = create_new_training(training)

    if created_training is None:
        raise InternalServerException('Error during saving training')

    calories = 0

    for _series in series:
        _series['training_id'] = created_training['training_id']
        exercises = _series.pop('exercises')

        created_series = create_new_series(_series)

        if created_series is None:
            raise InternalServerException('Error during saving series')

        for exercise in exercises:
            exercise['series_id'] = created_series['series_id']
            created_exercise = create_new_exercise(exercise)

            if created_exercise is None:
                raise InternalServerException('Error during saving exercises')

            calories += created_exercise['exercise_calories'] * created_series['iteration']

    if update_training(created_training['training_id'], training_calories=calories) is None:
        raise InternalServerException("Error XD")

    stored_training = get_training_by_args(training_id=created_training['training_id'])

    return Response({"training": stored_training}, status.HTTP_200_OK)
