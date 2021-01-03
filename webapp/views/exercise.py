from rest_framework.views import APIView

from webapp.controllers.exercise import create_exercise
from webapp.tools import handle_request


class Exercise(APIView):

    def post(self, request, series_id):
        return handle_request(create_exercise, request=request, series_id=series_id)
