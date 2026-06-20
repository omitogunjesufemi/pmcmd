from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseCRUDAPIView(APIView):
    service_class = None
    serializer_class = None
    input_serializer_class = None
    output_serializer_class = None
    resource_name = 'Resource'
    permission_classes = []
    permission_classes_by_method = {}

    def get_service(self):
        return self.service_class()

    def get_serializer_class(self):
        return self.serializer_class

    def get_input_serializer_class(self):
        return self.input_serializer_class or self.serializer_class

    def get_output_serializer_class(self):
        return self.output_serializer_class or self.serializer_class

    def get_permissions(self):
        permission_classes = self.permission_classes_by_method.get(
            self.request.method,
            self.permission_classes
        )
        return [permission() for permission in permission_classes]


class BaseListCreateAPIView(BaseCRUDAPIView):
    def get(self, request: Request):
        items = self.get_service().get_all()
        data = self.get_serializer_class()(items, many=True).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name}s retrieved successfully",
                "data": data,
            })

    def post(self, request: Request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_service().create(**serializer.validated_data)
        data = self.get_serializer_class()(instance).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name} created successfully",
                "data": data,
            },
            status=status.HTTP_201_CREATED
        )


class BaseRetrieveUpdateDeleteAPIView(BaseCRUDAPIView):
    lookup_url_kwarg = 'id'

    def get_object_id(self):
        return self.kwargs[self.lookup_url_kwarg]

    def get(self, request: Request, **kwargs):
        instance = self.get_service().get_by_id(self.get_object_id())
        data = self.get_serializer_class()(instance).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name} retrieved successfully",
                "data": data,
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request: Request, **kwargs):
        serializer = self.get_input_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_service().update(self.get_object_id(), **serializer.validated_data)
        data = self.get_output_serializer_class()(instance).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name} updated successfully",
                "data": data,
            },
            status=status.HTTP_200_OK
        )
