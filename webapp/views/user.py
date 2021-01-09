from rest_framework.views import APIView

from webapp.controllers.training import get_trainings_by_session_id
from webapp.controllers.user import *
from webapp.tools import handle_request


class ImageDownload(APIView):

    def get(self, request, image):
        return handle_request(download_image, request=request, image=image)


class UserLogout(APIView):

    def put(self, request):
        return handle_request(logout_user, request=request)


class UserDetails(APIView):

    def get(self, request, user_id=None):
        return handle_request(get_user_by_id, request=request, user_id=user_id)

    def delete(self, request, user_id=None):
        return handle_request(delete_user, request=request, user_id=user_id)

    def put(self, request, user_id=None):
        return handle_request(update_user, request=request, user_id=user_id, **request.data)


class UserLogin(APIView):

    def post(self, request):
        return handle_request(login_user, request=request)


class UserRegister(APIView):

    def post(self, request):
        return handle_request(register_user, request=request)


class UserList(APIView):

    def get(self, request):
        return handle_request(get_all_users, request=request)


class UserTrainings(APIView):

    def get(self, request, user_id):
        return handle_request(get_trainings_by_session_id, request=request, user_id=user_id)
