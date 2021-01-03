import hashlib
import mimetypes

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.crypto import get_random_string

from webapp.Errors import BadRequestException, NotFoundException
from webapp.models import User
from webapp.serializers import UserRawSerializer, UserSerializer
from webapp.tools import perform_get


def get_raw_user_by_args(**kwargs):
    user = perform_get(User.objects.get, **kwargs)

    if user is None:
        return None

    serializer = UserRawSerializer(user, many=False)
    return serializer.data


def get_user_by_args(**kwargs):
    user = perform_get(User.objects.get, **kwargs)

    if user is None:
        return None

    serializer = UserSerializer(user, many=False)

    return serializer.data


def get_all_users_by_args(**kwargs):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return serializer.data


def login_user_by_id(user_id, new_session_id):
    user = perform_get(User.objects.get, user_id=user_id)

    if user is None:
        return None

    user.session_id = new_session_id
    user.save(update_fields=['session_id'])

    return user


def logout_user_by_id(session_id):
    user = perform_get(User.objects.get, session_id=session_id)

    if user is None:
        return

    user.session_id = None
    user.save(update_fields=['session_id'])


def create_user(user):
    serializer = UserRawSerializer(data=user)

    if not serializer.is_valid():
        return None

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


def delete_user_by_id(user_id):
    user = perform_get(User.objects.get, user_id=user_id)

    if user is None:
        return False

    user.delete()

    return True


def update_user_by_id(user_id, **kwargs):
    user = perform_get(User.objects.get, user_id=user_id)

    if user is None:
        return None

    for k, v in kwargs.items():
        setattr(user, k, v)
    user.save(update_fields=kwargs.keys())

    return user


def update_user_photo(session_id, avatar):
    user = perform_get(User.objects.get, session_id=session_id)

    if user is None:
        return None

    user.avatar = avatar
    user.save()
    return user


def is_password_matching(password, **kwargs):
    db_user = perform_get(User.objects.get, **kwargs)

    if db_user is None:
        return False

    password_and_salt = password + db_user['salt']
    hashed_password_and_salt = hashlib.sha256(password_and_salt.encode(encoding="utf-8")).hexdigest()

    return hashed_password_and_salt == db_user['password']


def download_image(request, image):
    filename = image

    mime_type, _ = mimetypes.guess_type(filename)
    response = HttpResponse(filename, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
