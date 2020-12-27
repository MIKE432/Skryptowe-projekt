from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.controllers.training import get_training_by_id, create_training
from webapp.models import Training as _Training
from webapp.serializers import TrainingSerializer
from webapp.tools import handle_request


class Trainings(APIView):

    def get(self, request):
        training = _Training.objects.all()
        serializer = TrainingSerializer(training, many=False)
        return Response(serializer.data)


class TrainingDetails(APIView):

    def get(self, request, training_id):
        return handle_request(get_training_by_id, request=request, training_id=training_id)


class Training(APIView):

    def post(self, request):
        return handle_request(create_training, request=request)
