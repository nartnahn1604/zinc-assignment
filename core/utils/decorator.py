from functools import wraps
from rest_framework import status
from rest_framework.response import Response

def validate_request(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                params = schema(**request.GET.dict())
            except Exception as e:
                return Response({'message': "Invalid request parameters"}, status=status.HTTP_400_BAD_REQUEST)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator