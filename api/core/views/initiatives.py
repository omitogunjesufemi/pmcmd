from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from api.core.services.initiatives import InitiativeDocumentService, InitiativeTypeService
from api.core.serializers.initiatives import InitiativeDocumentOutputSerializer, InitiativeTypeSerializer


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
# Initiative Type View Actions
#--------------------------------------
class CreateInitiativeType(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Initiative Types'],
        request=InitiativeTypeSerializer,
    )
    def post(self, request: Request):
        serializer = InitiativeTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = (InitiativeTypeSerializer(
            InitiativeTypeService()
            .create_type(**serializer.validated_data))
                  .data)
        return Response(
            {
                'success':True,
                'message': 'Initiative Type created successfully',
                'data': result,
            },
            status=status.HTTP_201_CREATED
        )


class ListAllInitiativeTypes(APIView):
    @extend_schema(
        tags=['Initiative Types'],
    )
    def get(self, request: Request):
        initiative_types = InitiativeTypeService().get_all_types()
        result = InitiativeTypeSerializer(initiative_types, many=True).data
        return Response(
            {
                'success': True,
                'message': 'Initiative Types retrieved successfully',
                'data': result,
            },
            status=status.HTTP_200_OK
        )


class GetInitiativeType(APIView):
    @extend_schema(
        tags=['Initiative Types'],
    )
    def get(self, request: Request, type_id):
        initiative_type = InitiativeTypeService().get_type_by_id(type_id)
        result = InitiativeTypeSerializer(initiative_type).data
        return Response(
            {
                'success': True,
                'message': f'Initiative Type ({type_id}) retrieved successfully',
                'data': result,
            },
            status=status.HTTP_200_OK
        )
