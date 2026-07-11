from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import AllowAny
from api.core.serializers import CategorySerializer, StageRequirementTemplateInputSerializer, \
    StageRequirementTemplateOutputSerializer, InitiativeInputSerializer, InitiativeDocumentInputSerializer, \
    HandoverInputSerializer, HandoverOutputSerializer
from api.core.services.governance import HandoverService
from api.core.services.initiatives import InitiativeDocumentService, InitiativeTypeService, CategoryService, \
    StageRequirementTemplateService, InitiativeService
from api.core.serializers.initiatives import InitiativeDocumentOutputSerializer, InitiativeTypeSerializer, \
    InitiativeOutputSerializer, SubmitInitiativeDocumentSerializer, AdvanceInitiativeStageOutputSerializer
from api.core.views.base import BaseListCreateAPIView, BaseRetrieveUpdateAPIView, BaseListAPIView, \
    BaseRetrieveAPIView, BaseUpdateAPIView, BaseCreateAPIView, BaseCreateNoSerializerAPIView
from utils.constants import PENDING_DOC_PARAM, BLOCKING_DOC_PARAM, DOC_NAME_PARAM, INITIATIVE_LIST_PARAMS, Stage_Param, \
    Status_Param


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
        'GET': [IsAuthenticated],
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
        parameters=INITIATIVE_LIST_PARAMS,
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

    def get_list_service_kwargs(self):
        return {
            'category_id': self.request.query_params.get('category_id', None),
            'initiative_type_id': self.request.query_params.get('initiative_type_id', None),
            'stage': self.request.query_params.get('stage', None),
            'status': self.request.query_params.get('status', None),
            'page': self.request.query_params.get('page', None),
            'owner': self.request.user if self.request.user.is_authenticated else None,
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
    retrieve_service_method = "get_by_id_and_owner"
    input_serializer_class = InitiativeInputSerializer
    output_serializer_class = InitiativeOutputSerializer
    resource_name = "Initiative"
    lookup_url_kwarg = "initiative_id"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [AllowAny]
    }

    def get_retrieve_service_kwargs(self):
        return {
            'owner': self.request.user if self.request.user.is_authenticated else None,
        }

    def get_update_service_kwargs(self, serializer):
        return {
            **serializer.validated_data,
            'owner': self.request.user if self.request.user.is_authenticated else None
        }


@extend_schema(
    tags=["Initiatives"],
    responses=AdvanceInitiativeStageOutputSerializer
)
class AdvanceInitiativeStageView(BaseCreateNoSerializerAPIView):
    service_class = InitiativeService
    create_service_method = "advance_stage"
    output_serializer_class = AdvanceInitiativeStageOutputSerializer
    resource_name = "Initiative"
    lookup_url_kwarg = "initiative_id"
    permission_classes = [AllowAny]
    response_message = f"{resource_name} advance to the next stage successfully"


@extend_schema(
    tags=['Initiatives'],
    request=HandoverInputSerializer,
    responses=HandoverOutputSerializer
)
class InitiativeHandoverView(BaseCreateAPIView):
    service_class = HandoverService
    create_service_method = "create_handover"
    input_serializer_class = HandoverInputSerializer
    output_serializer_class = HandoverOutputSerializer
    resource_name = "Initiative Handover"
    lookup_url_kwarg = "initiative_id"
    permission_classes = [AllowAny]

    def get_create_service_kwargs(self, serializer):
        return {
            **serializer.data,
            'initiative_id': self.get_object_id(),
            'from_user': self.request.user if self.request.user.is_authenticated else None,
        }


# ---------------------------------------
# Initiative Document CRUD View Actions |
# ---------------------------------------
@extend_schema(
    tags=["Initiative Documents"],
    responses=InitiativeDocumentOutputSerializer(many=True)
)
@extend_schema_view(
    get=extend_schema(
        parameters=[Stage_Param, Status_Param],
    ),
    post=extend_schema(
        request=InitiativeDocumentInputSerializer,
    )
)
class InitiativeDocumentListView(BaseListCreateAPIView):
    service_class = InitiativeDocumentService
    list_service_method = "get_documents_for_initiative"
    create_service_method = "add_custom_document"
    input_serializer_class = InitiativeDocumentInputSerializer
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    lookup_url_kwarg = "initiative_id"
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [AllowAny]
    }

    def get_list_service_kwargs(self):
        return {
            'initiative_id': self.get_object_id(),
            'owner': self.request.user if self.request.user.is_authenticated else None,
            'status': self.request.query_params.get('status', None),
            'stage': self.request.query_params.get('stage', None)
        }

    def get_create_service_kwargs(self, serializer):
        return {
            **serializer.validated_data,
            'initiative_id': self.get_object_id(),
            'owner': self.request.user if self.request.user.is_authenticated else None,
        }


@extend_schema(
    tags=["Initiative Documents"],
    responses=InitiativeDocumentOutputSerializer(many=True)
)
class DocumentsForAInitiativeListView(BaseListAPIView):
    service_class = InitiativeDocumentService
    list_service_method = "get_documents_for_initiative"
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    permission_classes_by_method = {
        'GET': [AllowAny],
    }
    lookup_url_kwarg = 'initiative_id'

    def get_list_service_kwargs(self):
        return {
            'initiative_id': self.get_object_id()
        }


@extend_schema(
    tags=["Initiative Documents"],
    parameters=BLOCKING_DOC_PARAM,
    responses=InitiativeDocumentOutputSerializer(many=True)
)
class BlockingDocumentsForInitiativeView(BaseListAPIView):
    service_class = InitiativeDocumentService
    list_service_method = "get_blocking_document_for_initiative"
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    permission_classes_by_method = {
        'GET': [AllowAny],
    }

    def get_list_service_kwargs(self):
        return {
            'initiative_id': self.request.query_params.get('initiative_id', None),
            'stage': self.request.query_params.get('stage', None),
        }


@extend_schema(
    tags=["Initiative Documents"],
    request=SubmitInitiativeDocumentSerializer,
    responses=InitiativeDocumentOutputSerializer
)
class SubmitDocumentForInitiativeView(BaseUpdateAPIView):
    service_class = InitiativeDocumentService
    update_service_method = "submit_document"
    input_serializer_class = SubmitInitiativeDocumentSerializer
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    lookup_url_kwarg = "initiative_id"

    def get_update_service_kwargs(self, serializer):
        return {
            'document_name': self.request.data.get('document_name', None),
            'user': self.request.user
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


@extend_schema(
    tags=["Initiative Documents"],
    responses=InitiativeDocumentOutputSerializer(many=True)
)
class OwnerInitiativeDocumentListView(BaseListAPIView):
    service_class = InitiativeDocumentService
    list_service_method = "get_documents_for_owner"
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    permission_classes_by_method = {
        'GET': [AllowAny],
    }

    def get_list_service_kwargs(self):
        return {
            'owner': self.request.user
        }


@extend_schema(
    tags=["Initiative Documents"],
    parameters=PENDING_DOC_PARAM,
    responses=InitiativeDocumentOutputSerializer(many=True)
)
class PendingApprovalsInitiativeDocumentListView(BaseListAPIView):
    service_class = InitiativeDocumentService
    list_service_method = "get_pending_approvals_for_initiative"
    output_serializer_class = InitiativeDocumentOutputSerializer
    resource_name = "Initiative Document"
    permission_classes_by_method = {
        'GET': [AllowAny],
    }

    def get_list_service_kwargs(self):
        return {
            'initiative_id': self.request.query_params.get('initiative_id', None)
        }
