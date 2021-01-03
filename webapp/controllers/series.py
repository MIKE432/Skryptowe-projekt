from rest_framework import status
from rest_framework.response import Response

from webapp.models import Training, User
from webapp.services.series import create_new_series
from webapp.tools import perform_get, BadRequestException, UnauthorizedException, ForbiddenException


def create_series(request, training_id=None):
    session_id = request.query_params['session_id']
    training = perform_get(Training.objects.get, training_id=training_id)
    request_body = dict(request.data)

    if session_id is None:
        raise UnauthorizedException("You need to be logged")

    if training is None:
        raise BadRequestException("Invalid training id")

    user = perform_get(User.objects.get, session_id=session_id)

    if user is None:
        raise UnauthorizedException("You need to be logged")

    if user.user_id != training.created_by.user_id:
        raise ForbiddenException("You don`t have permission to modify that training")

    request_body['training_id'] = training_id
    created_series = create_new_series(request_body)

    if created_series is None:
        raise BadRequestException("Invalid exercise format")

    return Response(created_series, status.HTTP_200_OK)

