from webapp.Errors import BadRequestException
from webapp.serializers import RawSeriesSerializer


def create_new_series(series):

    serializer = RawSeriesSerializer(data=series)

    if not serializer.is_valid():
        return None

    serializer.save()

    return serializer.data
