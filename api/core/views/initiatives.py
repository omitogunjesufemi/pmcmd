from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.serializers import CategorySerializer, StageRequirementTemplateInputSerializer, \
    StageRequirementTemplateOutputSerializer, InitiativeInputSerializer, InitiativeDocumentInputSerializer
from api.core.services.initiatives import InitiativeDocumentService, InitiativeTypeService, CategoryService, \
    StageRequirementTemplateService, InitiativeService
from api.core.serializers.initiatives import InitiativeDocumentOutputSerializer, InitiativeTypeSerializer, \
    InitiativeOutputSerializer
from api.core.views.base import BaseListCreateAPIView, BaseRetrieveUpdateAPIView, BaseListAPIView, \
    BaseRetrieveAPIView


# -------------------------------------
# Initiative CRUD Type View Actions   |
# -------------------------------------
@extend_schema(
    tags=["Initiative Types"]
)
@extend_schema_view(
    get=extend_schema(
        responses=InitiativeTypeSerializer(many=True)
    ),
    post=extend_schema(
        request=InitiativeTypeSerializer,
        responses=InitiativeTypeSerializer,
    ),
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
@extend_schema_view(
    get=extend_schema(
        responses=InitiativeTypeSerializer
    ),
    patch=extend_schema(
        request=InitiativeTypeSerializer,
        responses=InitiativeTypeSerializer,
    ),
)
class InitiativeTypeDetailView(BaseRetrieveUpdateAPIView):
    service_class = InitiativeTypeService
    serializer_class = InitiativeTypeSerializer
    resource_name = "Initiative Type"
    lookup_url_kwarg = "type_id"

    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [AllowAny]
    }


# ------------------------------------
# Category CRUD View Actions         |
# ------------------------------------
@extend_schema(
    tags=["Category"]
)
@extend_schema_view(
    get=extend_schema(
        responses=CategorySerializer(many=True)
    ),
    post=extend_schema(
        request=CategorySerializer,
        responses=CategorySerializer,
    ),
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
@extend_schema_view(
    get=extend_schema(
        responses=CategorySerializer
    ),
    patch=extend_schema(
        request=CategorySerializer,
        responses=CategorySerializer,
    ),
)
class CategoryDetailView(BaseRetrieveUpdateAPIView):
    service_class = CategoryService
    serializer_class = CategorySerializer
    resource_name = "Category"
    lookup_url_kwarg = "category_id"

    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [AllowAny]
    }


# ------------------------------------
# S.Reqmt.Template CRUD View Actions |
# ------------------------------------
@extend_schema(
    tags=["Requirement Templates"]
)
@extend_schema_view(
    get=extend_schema(
        responses=StageRequirementTemplateOutputSerializer(many=True)
    ),
    post=extend_schema(
        request=StageRequirementTemplateInputSerializer,
        responses=StageRequirementTemplateOutputSerializer,
    ),
)
class RequirementTemplateListCreateView(BaseListCreateAPIView):
    service_class = StageRequirementTemplateService
    input_serializer_class = StageRequirementTemplateInputSerializer
    output_serializer_class = StageRequirementTemplateOutputSerializer
    resource_name = "Stage Requirement Template"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [AllowAny]
    }


@extend_schema(
    tags=["Requirement Templates"]
)
@extend_schema_view(
    get=extend_schema(
        responses=StageRequirementTemplateOutputSerializer
    ),
    patch=extend_schema(
        request=StageRequirementTemplateInputSerializer,
        responses=StageRequirementTemplateOutputSerializer,
    ),
)
class RequirementTemplateDetailView(BaseRetrieveUpdateAPIView):
    service_class = StageRequirementTemplateService
    input_serializer_class = StageRequirementTemplateInputSerializer
    output_serializer_class = StageRequirementTemplateOutputSerializer
    resource_name = "Stage Requirement Template"
    lookup_url_kwarg = "template_id"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [AllowAny]
    }


# ------------------------------------
# Initiative CRUD View Actions       |
# ------------------------------------
@extend_schema(
    tags=["Initiatives"]
)
@extend_schema_view(
    get=extend_schema(
        responses=InitiativeOutputSerializer(many=True)
    ),
    post=extend_schema(
        request=InitiativeInputSerializer,
        responses=InitiativeOutputSerializer
    )
)
class InitiativeListCreateView(BaseListCreateAPIView):
    service_class = InitiativeService
    input_serializer_class = InitiativeInputSerializer
    output_serializer_class = InitiativeOutputSerializer
    resource_name = "Initiative"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [AllowAny]
    }

    def get_create_service_kwargs(self, serializer):
        return {
            **serializer.validated_data,
            'user': self.request.user if self.request.user.is_authenticated else None
        }


@extend_schema(
    tags=["Initiatives"]
)
@extend_schema_view(
    get=extend_schema(
        responses=InitiativeOutputSerializer
    ),
    patch=extend_schema(
        request=InitiativeInputSerializer,
        responses=InitiativeOutputSerializer
    )
)
class InitiativeDetailUpdateView(BaseRetrieveUpdateAPIView):
    service_class = InitiativeService
    input_serializer_class = InitiativeInputSerializer
    output_serializer_class = InitiativeOutputSerializer
    resource_name = "Initiative"
    lookup_url_kwarg = "initiative_id"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [AllowAny]
    }


# ------------------------------------
# Initiative View Actions
# ------------------------------------
@extend_schema(
    tags=["Initiative Documents"],
    responses=InitiativeDocumentOutputSerializer
)
class InitiativeDocumentListView(BaseListAPIView):
    service_class = InitiativeDocumentService
    input_serializer_class = InitiativeDocumentInputSerializer
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    permission_classes_by_method = {
        'GET': [AllowAny],
    }


@extend_schema(
    tags=["Initiative Documents"],
    responses=InitiativeDocumentOutputSerializer
)
class InitiativeDocumentDetailView(BaseRetrieveAPIView):
    service_class = InitiativeDocumentService
    input_serializer_class = InitiativeDocumentInputSerializer
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    lookup_url_kwarg = "document_id"
    permission_classes_by_method = {
        'GET': [AllowAny],
    }

# ------------------------------------
# Initiative Document CRUD View Actions
# ------------------------------------
