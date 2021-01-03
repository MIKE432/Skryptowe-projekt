from webapp.serializers import RawSeriesSerializer, RawExerciseSerializer


def create_new_exercise(exercise):

    serializer = RawExerciseSerializer(data=exercise)

    if not serializer.is_valid():
        return None

    serializer.save()

    return serializer.data


