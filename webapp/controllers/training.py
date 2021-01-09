from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from webapp.Errors import NotFoundException, BadRequestException, UnauthorizedException, InternalServerException, \
    ForbiddenException
from webapp.controllers.exercise import prepare_exercise
from webapp.services.exercise import create_new_exercise
from webapp.services.series import create_new_series
from webapp.services.training import create_new_training, get_training_by_args, update_training, \
    get_all_trainings_by_session_id, delete_training, get_user_trainings_by_id
from webapp.services.user import get_user_by_args


def get_all_trainings(request):
    query_params = request.query_params
    training_calories_min = query_params.get('calories_min') if query_params.get('calories_min') is not None else 0
    training_calories_max = query_params.get('calories_max') if query_params.get(
        'calories_max') is not None else 2147483647
    training_name = query_params.get('name') if query_params.get('name') is not None else ""
    training_type = query_params.get('type') if query_params.get('type') is not None else ""
    return Response(
        get_all_trainings_by_session_id(query_params['session_id'], training_calories_min=training_calories_min,
                                        training_calories_max=training_calories_max, training_name=training_name,
                                        training_type=training_type), status.HTTP_200_OK)


def get_training_by_id(request, training_id):
    training = get_training_by_args(training_id=training_id)
    query_params = request.query_params

    if training is None:
        raise NotFoundException("There is no training with given id")

    if not training['is_public'] and 'session_id' not in query_params:
        raise UnauthorizedException("You don`t have permission to read this resource(no session_id passed)")

    user = get_user_by_args(
        session_id=request.query_params['session_id']) if 'session_id' in request.query_params else None

    if not training['is_public'] and user is None:
        raise UnauthorizedException("You don`t have permission to read this resource")

    if not training['is_public'] and user['user_id'] != training['created_by']:
        raise ForbiddenException("You don`t have permission to read this resource")

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
        raise InternalServerException("Error during saving training")

    stored_training = get_training_by_args(training_id=created_training['training_id'])

    return Response({"training": stored_training}, status.HTTP_200_OK)


def create_raw_training(request):
    request_body = dict(request.data)
    query_params = request.query_params

    if 'session_id' not in query_params:
        raise UnauthorizedException("You need to be logged")

    user = get_user_by_args(session_id=query_params['session_id'])

    if user is None:
        raise UnauthorizedException("Invalid session id")

    request_body['created_by'] = user['user_id']

    created_training = create_new_training(request_body)

    if created_training is None:
        raise BadRequestException('Cannot create training')

    return Response(created_training, status.HTTP_200_OK)


def delete_training_by_id(request, training_id):
    query_params = request.query_params

    if 'session_id' not in query_params:
        raise UnauthorizedException("You need to be logged")

    user = get_user_by_args(session_id=query_params['session_id'])

    if user is None:
        raise UnauthorizedException("Invalid session id")

    if delete_training(training_id) is None:
        raise NotFoundException('Training with given id does not exist')

    return Response({"code": 200}, status.HTTP_200_OK)


def update_training_by_id(request, training_id):
    request_body = dict(request.data)
    query_params = request.query_params

    if 'session_id' not in query_params:
        raise UnauthorizedException("You need to be logged")

    user = get_user_by_args(session_id=query_params['session_id'])

    if user is None:
        raise UnauthorizedException("Invalid session id")

    if update_training(training_id, **request_body) is None:
        raise InternalServerException("Cannot update training")


def get_trainings_by_session_id(request, user_id):
    query_params = request.query_params

    if 'session_id' not in query_params:
        raise UnauthorizedException("You need to be logged")
    trainings = get_user_trainings_by_id(query_params['session_id'], user_id)

    return Response(trainings, status.HTTP_200_OK)
