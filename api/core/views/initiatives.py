from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.serializers import CategorySerializer
from api.core.services.initiatives import InitiativeDocumentService, InitiativeTypeService, CategoryService
from api.core.serializers.initiatives import InitiativeDocumentOutputSerializer, InitiativeTypeSerializer
from api.core.views.base import BaseListCreateAPIView, BaseRetrieveUpdateDeleteAPIView


class GetAllInitiativeDocuments(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        documents = InitiativeDocumentService().get_documents()
        data = InitiativeDocumentOutputSerializer(documents, many=True).data
        return Response(
            {
                'success': True,
                'message': 'Initiative Document retrieved successfully',
                'data': data,
            },
            status=status.HTTP_200_OK
        )


# -------------------------------------
# Initiative CRUD Type View Actions
# -------------------------------------
@extend_schema(
    tags=["Initiative Types"]
)
class InitiativeTypeListCreateView(BaseListCreateAPIView):
    service_class = InitiativeTypeService
    serializer_class = InitiativeTypeSerializer
    resource_name = "Initiative Type"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [AllowAny]
    }


@extend_schema(
    tags=["Initiative Types"]
)
class InitiativeTypeDetailView(BaseRetrieveUpdateDeleteAPIView):
    service_class = InitiativeTypeService
    serializer_class = InitiativeTypeSerializer
    resource_name = "Initiative Type"
    lookup_url_kwarg = "type_id"

    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [AllowAny]
    }


# ------------------------------------
# Category CRUD View Actions              |
# ------------------------------------
@extend_schema(
    tags=["Category"]
)
class CategoryListCreateView(BaseListCreateAPIView):
    service_class = CategoryService
    serializer_class = CategorySerializer
    resource_name = "Category"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [AllowAny]
    }


@extend_schema(
    tags=["Category"]
)
class CategoryDetailView(BaseRetrieveUpdateDeleteAPIView):
    service_class = CategoryService
    serializer_class = CategorySerializer
    resource_name = "Category"
    lookup_url_kwarg = "category_id"

    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [AllowAny]
    }
