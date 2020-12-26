import hashlib

from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.Errors import *
from webapp.models import User
from webapp.serializers import UserRawSerializer, UserSerializer
from webapp.tools import handle_request


def register_user(request):
    serializer = UserRawSerializer(data=request.data)

    if not serializer.is_valid():
        raise BadRequestException("User with given nickname exists")

    serializer.save()
    serializer.data.pop('password')
    user = serializer.data
    del user['password']
    del user['salt']

    return Response(user, status.HTTP_201_CREATED)


def logout_user(request):
    if "session_id" not in request.data:
        raise BadRequestException("No session id")

    user = User.objects.get(session_id=request.data['session_id'])

    user.session_id = None
    user.save(update_fields=['session_id'])

    return Response({status: 200}, status.HTTP_200_OK)


def login_user(request):
    user = User.objects.get(nick=request.data['nick'])
    db_serializer = UserRawSerializer(user, many=False)

    db_user = db_serializer.data

    password_and_salt = request.data['password'] + db_user['salt']
    hashed_password_and_salt = hashlib.sha256(password_and_salt.encode(encoding="utf-8")).hexdigest()

    if hashed_password_and_salt == db_user['password']:
        raise UnauthorizedException("Invalid nick or password")

    return_user = db_user

    while True:
        session_id = get_random_string(25)
        try:
            User.objects.get(session_id=session_id)
        except ObjectDoesNotExist:
            user.session_id = session_id
            user.save(update_fields=['session_id'])
            del return_user['password']
            del return_user['salt']

            return Response(return_user, status.HTTP_200_OK)


def get_user_by_id(request, user_id):
    if user_id is None:
        raise BadRequestException("No user details")

    user = User.objects.get(pk=user_id)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status.HTTP_200_OK)


def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
