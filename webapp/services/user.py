from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string

from webapp.Errors import BadRequestException, NotFoundException
from webapp.models import User
from webapp.serializers import UserRawSerializer, UserSerializer
from webapp.tools import perform_get


def get_raw_user_by_args(**kwargs):
    user = perform_get(User.objects.get, **kwargs)

    if user is None:
        raise NotFoundException("There is no user with given id")

    serializer = UserRawSerializer(user, many=False)
    return serializer.data


def get_user_by_args(**kwargs):
    user = perform_get(User.objects.get, **kwargs)

    if user is None:
        raise NotFoundException("There is no user with given id")

    serializer = UserSerializer(user, many=False)

    return serializer.data


def get_all_users_by_args(**kwargs):

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return serializer.data


def login_user_by_id(user_id, new_session_id):
    user = perform_get(User.objects.get, user_id=user_id)

    if user is None:
        raise NotFoundException("There is no user with given id")

    user.session_id = new_session_id
    user.save(update_fields=['session_id'])
    return user


def logout_user_by_id(session_id):
    user = perform_get(User.objects.get, session_id=session_id)
    if user is None:
        raise NotFoundException("There is no user with given session id")
    user.session_id = None
    user.save(update_fields=['session_id'])


def create_user(user):
    serializer = UserRawSerializer(data=user)

    if not serializer.is_valid():
        raise BadRequestException("User with given nickname exists")

    serializer.save()

    return serializer.data


def map_user_to_response_model(user):
    if 'password' in user:
        del user['password']
    if 'salt' in user:
        del user['salt']

    return user


def generate_session_id():
    while True:
        session_id = get_random_string(25)
        try:
            User.objects.get(session_id=session_id)
        except ObjectDoesNotExist:
            return session_id
