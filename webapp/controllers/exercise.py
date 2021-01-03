from rest_framework import status
from rest_framework.response import Response

from webapp.Errors import BadRequestException, UnauthorizedException, ForbiddenException
from webapp.models import User, Series, Training
from webapp.services.exercise import create_new_exercise
from webapp.tools import perform_get


def create_exercise(request, series_id=None):
    request_body = prepare_exercise(dict(request.data))

    query_params = request.query_params
    if 'session_id' not in query_params:
        raise UnauthorizedException("You need to be logged to create training")

    if series_id is None:
        raise BadRequestException("No series id provided")
    user = perform_get(User.objects.get, session_id=query_params['session_id'])
    series = perform_get(Series.objects.get, series_id=series_id)

    if user is None:
        raise UnauthorizedException("You need to be logged to create training")

    if series is None:
        raise BadRequestException("Invalid series id")

    training = perform_get(Training.objects.get, training_id=series.training_id.training_id)

    if training.created_by.user_id != user.user_id:
        raise ForbiddenException("You don`t have permission to modify that training")

    request_body['series_id'] = series_id
    if 'photo' not in request_body or request_body['photo'] == '':
        request_body['photo'] = None

    created_exercise = create_new_exercise(request_body)

    if created_exercise is None:
        raise BadRequestException("Invalid exercise format")

    return Response(created_exercise, status.HTTP_200_OK)


def prepare_exercise(raw_exercise):
    e = raw_exercise
    for k, v in e.items():
        e[k] = v[0]

    return e
