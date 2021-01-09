import hashlib

from rest_framework import status
from rest_framework.response import Response
from webapp.Errors import *
from webapp.services.user import *


def register_user(request):
    body = request.data

    if 'name' not in body:
        raise BadRequestException("Name is required")

    if 'surname' not in body:
        raise BadRequestException("Surname is required")

    if 'password' not in body:
        raise BadRequestException("Surname is required")

    user = create_user(request.data)

    if user is None:
        raise BadRequestException("User with given nickname exists")

    session_id = generate_session_id()

    created_user = login_user_by_id(user['user_id'], session_id)

    if created_user is None:
        raise InternalServerException("Cannot log in user")

    return_user = user

    return_user['session_id'] = session_id

    return Response(map_user_to_response_model(user), status.HTTP_201_CREATED)


def logout_user(request):
    if "session_id" not in request.data:
        raise BadRequestException("No session id")

    logout_user_by_id(request.data["session_id"])

    return Response({"code": 200}, status.HTTP_200_OK)


def login_user(request):
    request_body = request.data

    if 'nick' not in request_body or 'password' not in request_body:
        raise BadRequestException("No nick or password provided")

    db_user = get_raw_user_by_args(nick=request.data['nick'])

    if db_user is None:
        raise NotFoundException("There is no user with given id")

    password_and_salt = request.data['password'] + db_user['salt']
    hashed_password_and_salt = hashlib.sha256(password_and_salt.encode(encoding="utf-8")).hexdigest()

    if hashed_password_and_salt != db_user['password']:
        raise UnauthorizedException("Invalid nick or password")

    return_user = db_user

    session_id = generate_session_id()
    created_user = login_user_by_id(db_user['user_id'], session_id)

    if created_user is None:
        raise InternalServerException("Cannot log in user")

    return_user['session_id'] = session_id

    return Response(map_user_to_response_model(return_user), status.HTTP_200_OK)


def get_user_by_id(request, user_id):
    if user_id is None:
        raise BadRequestException("No user details")

    user = get_user_by_args(pk=user_id)

    if user is None:
        raise NotFoundException("There is no user with given id")

    return Response(user, status.HTTP_200_OK)


def get_all_users(request):
    users = get_all_users_by_args()
    return Response(users, status.HTTP_200_OK)


def update_user(request, user_id, **kwargs):
    if 'session_id' not in request.query_params:
        raise BadRequestException('You have to provide session id')

    if 'avatar' not in kwargs:
        raise BadRequestException('Avatar is required')

    user = update_user_photo(request.query_params['session_id'], kwargs['avatar'][0])

    if user is None:
        raise InternalServerException("Cannot update user")

    return Response({"code": 200}, status.HTTP_200_OK)


def delete_user(request, user_id):
    query_params = request.query_params

    if 'session_id' not in query_params:
        raise BadRequestException("You need provide session_id to remove that account")

    if not delete_user_by_id(user_id):
        raise UnauthorizedException("Cannot delete account")

    return Response({"code": 200}, status.HTTP_200_OK)
