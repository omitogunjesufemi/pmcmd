from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.serializers import CategorySerializer, StageRequirementTemplateInputSerializer, \
    StageRequirementTemplateOutputSerializer, InitiativeInputSerializer
from api.core.services.initiatives import InitiativeDocumentService, InitiativeTypeService, CategoryService, \
    StageRequirementTemplateService, InitiativeService
from api.core.serializers.initiatives import InitiativeDocumentOutputSerializer, InitiativeTypeSerializer, \
    InitiativeOutputSerializer
from api.core.views.base import BaseListCreateAPIView, BaseRetrieveUpdateDeleteAPIView


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
class CategoryDetailView(BaseRetrieveUpdateDeleteAPIView):
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
class RequirementTemplateDetailView(BaseRetrieveUpdateDeleteAPIView):
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
        responses=InitiativeOutputSerializer
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

    def get_service_context(self):
        return {'user': self.request.user}


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
class InitiativeDetailUpdateView(BaseRetrieveUpdateDeleteAPIView):
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
# Initiative Document CRUD View Actions       |
# ------------------------------------