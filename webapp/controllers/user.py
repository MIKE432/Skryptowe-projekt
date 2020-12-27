import hashlib

from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from webapp.Errors import *
from webapp.services.user import *


def register_user(request):
    user = create_user(request.data)
    return Response(map_user_to_response_model(user), status.HTTP_201_CREATED)


def logout_user(request):
    if "session_id" not in request.data:
        raise BadRequestException("No session id")

    logout_user_by_id(request.data["session_id"])

    return Response({"status": 200}, status.HTTP_200_OK)


def login_user(request):
    db_user = get_raw_user_by_args(nick=request.data['nick'])

    password_and_salt = request.data['password'] + db_user['salt']
    hashed_password_and_salt = hashlib.sha256(password_and_salt.encode(encoding="utf-8")).hexdigest()

    if hashed_password_and_salt != db_user['password']:
        raise UnauthorizedException("Invalid nick or password")

    return_user = db_user

    session_id = generate_session_id()
    login_user_by_id(db_user['user_id'], session_id)
    return_user['session_id'] = session_id

    return Response(map_user_to_response_model(return_user), status.HTTP_200_OK)


def get_user_by_id(request, user_id):
    if user_id is None:
        raise BadRequestException("No user details")

    user = get_user_by_args(pk=user_id)

    return Response(user, status.HTTP_200_OK)


def get_all_users(request):
    users = get_all_users_by_args()
    return Response(users, status.HTTP_200_OK)
