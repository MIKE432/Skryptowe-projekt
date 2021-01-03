from rest_framework.views import APIView

from webapp.controllers.series import create_series
from webapp.tools import handle_request


class Series(APIView):

    def post(self, request, training_id):
        return handle_request(create_series, request=request, training_id=training_id)
