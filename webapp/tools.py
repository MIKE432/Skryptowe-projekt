import random
import string

from rest_framework import status
from rest_framework.response import Response

from webapp.Errors import *


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def handle_request(func, **kwargs):
    try:
        return func(**kwargs)

    except BadRequestException as e:
        return Response({"code": e.code, "message": e.msg}, e.code)
    except NotFoundException as e:
        return Response({"code": e.code, "message": e.msg}, e.code)
    except UnauthorizedException as e:
        return Response({"code": e.code, "message": e.msg}, e.code)
    except ForbiddenException as e:
        return Response({"code": e.code, "message": e.msg}, e.code)
    except InternalServerException as e:
        return Response({"code": e.code, "message": e.msg}, e.code)
    except HttpException as e:
        return Response({"code": e.code, "message": e.msg}, e.code)
    except Exception as e:
        return Response({"code": 500, "message": e}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrainingTypes:
    AEROBIC: str = "AEROBIC"
    STRENGTH: str = "STRENGTH"
    STRETCHING: str = "STRETCHING"
    BALANCE: str = "BALANCE"
    RECOVERY: str = "RECOVERY"
    CIRCUIT: str = "CIRCUIT"
    FUNCTIONAL: str = "FUNCTIONAL"
    HIIT: str = "HIIT"
    INTERVAL: str = "INTERVAL"
    CARDIO: str = "CARDIO"
    TABATA: str = "TABATA"
    SUPERSET: str = "SUPERSET"
    OTHER: str = "OTHER"


class ExerciseTypes:
    WARMUP: str = "WARMUP"
    STRETCHING: str = "STRETCHING"
    COOLDOWN: str = "COOLDOWN"
    CHEST: str = "CHEST"
    ABS: str = "ABS"
    ARM: str = "ARM"
    LEG: str = "LEG"
    SHOULDER: str = "SHOULDER"
    BACK: str = "BACK"
    OTHER: str = "OTHER"

