from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.controllers.training import get_training_by_id
from webapp.models import Training as _Training
from webapp.serializers import TrainingSerializer
from webapp.tools import handle_request


class TrainingList(APIView):

    def get(self, request):
        training = _Training.objects.all()
        serializer = TrainingSerializer(training, many=False)
        return Response(serializer.data)


#will be training details
class Training(APIView):

    def get(self, request, training_id):
        return handle_request(get_training_by_id, request=request, training_id=training_id)

    def post(self):
        pass