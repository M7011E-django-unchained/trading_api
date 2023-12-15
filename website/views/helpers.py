import hashlib
from django.core.cache import cache
from rest_framework.exceptions import APIException


class IdempotencyException(APIException):
    status_code = 201
    default_detail = "Duplicate request, item already created"


def idempotent_check(request):
    key = hashlib.blake2b(
        f"{request.user.id}, {request.path}, {request.data}".encode("utf-8")
    ).hexdigest()

    is_cache = cache.get(key)

    if is_cache:
        return False  # duplicate request

    expiary = 60 * 15  # 15 min
    cache.set(key, True, expiary)

    return True  # new request
