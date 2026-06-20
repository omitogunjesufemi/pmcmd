from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status

def pmd_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        detail = str(exc) if settings.DEBUG else 'Internal server error.'
        return Response(
            {
                'success': False,
                'errors': {
                    'detail': detail
                },
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response.data = {
        'success': False,
        'errors': response.data,
        'status_code': response.status_code
    }
    return response