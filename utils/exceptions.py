from rest_framework.exceptions import APIException, ParseError
from rest_framework import status


class ServiceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business rule violation'
    default_code = 'service_error'


class InvalidStateTransitionException(ServiceException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Invalid state transition."
    default_code = "invalid_state_transition"

class BlockingDocumentException(ServiceException):
    document_count = 0
    default_code = "stage_advancement_blocked"
    default_detail = f"Cannot advance stage - {document_count} required documents are pending"