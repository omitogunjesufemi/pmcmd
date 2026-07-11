from idlelib.rpc import response_queue

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import PMCMDPagination


class BaseCRUDAPIView(APIView):
    service_class = None
    list_service_method = "get_all"
    retrieve_service_method = "get_by_id"
    create_service_method = "create"
    update_service_method = "update"

    serializer_class = None
    input_serializer_class = None
    output_serializer_class = None
    resource_name = 'Resource'
    permission_classes = []
    permission_classes_by_method = {}

    lookup_url_kwarg = 'id'

    def get_object_id(self):
        return self.kwargs[self.lookup_url_kwarg]

    def get_service(self):
        if self.service_class is None:
            raise NotImplementedError("service_class must be set.")
        return self.service_class()

    def call_service_method(self, method_name, *args, **kwargs):
        service = self.get_service()
        method = getattr(service, method_name, None)
        if method is None:
            raise NotImplementedError("service does not have this method.")
        return method(*args, **kwargs)

    def get_list_service_args(self):
        return []

    def get_list_service_kwargs(self):
        return {}

    def get_retrieve_service_args(self):
        return [self.get_object_id()]

    def get_retrieve_service_kwargs(self):
        return {}

    def get_create_service_args(self, serializer):
        return []

    def get_create_service_kwargs(self, serializer):
        return serializer.validated_data

    def get_update_service_args(self, serializer):
        return [self.get_object_id()]

    def get_update_service_kwargs(self, serializer):
        return serializer.validated_data

    def get_serializer_class(self):
        return self.serializer_class

    def get_input_serializer_class(self):
        serializer_c = self.input_serializer_class or self.serializer_class
        if serializer_c is None:
            raise NotImplementedError("The input serializer was not implemented.")
        return self.input_serializer_class or self.serializer_class

    def get_output_serializer_class(self):
        serializer_c = self.output_serializer_class or self.serializer_class
        if serializer_c is None:
            raise NotImplementedError("The output serializer was not implemented.")
        return self.output_serializer_class or self.serializer_class

    def get_permissions(self):
        permission_classes = self.permission_classes_by_method.get(
            self.request.method,
            self.permission_classes
        )
        return [permission() for permission in permission_classes]



class BaseListAPIView(BaseCRUDAPIView):
    def get(self, request: Request, **kwargs):
        items = self.call_service_method(self.list_service_method,
                                         *self.get_list_service_args(),
                                         **self.get_list_service_kwargs())
        paginator: PMCMDPagination = PMCMDPagination()
        page = paginator.paginate_queryset(queryset=items, request=request, view=self)

        if page is not None:
            data = self.get_output_serializer_class()(page, many=True).data
            result = paginator.get_paginated_response(data)

            result.data = {
                "success": True,
                "message": f"{self.resource_name}s retrieved successfully",
                **result.data
            }
            return result

        data = self.get_output_serializer_class()(items, many=True).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name}s retrieved successfully",
                "data": data,
                "count": len(data)
            },
            status=status.HTTP_200_OK
        )


class BaseCreateAPIView(BaseCRUDAPIView):
    def post(self, request: Request, **kwargs):
        serializer = self.get_input_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.call_service_method(self.create_service_method,
                                            *self.get_create_service_args(serializer),
                                            **self.get_create_service_kwargs(serializer))
        data = self.get_output_serializer_class()(instance).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name} created successfully",
                "data": data,
            },
            status=status.HTTP_201_CREATED
        )


class BaseCreateNoSerializerAPIView(BaseCRUDAPIView):
    response_message = "Updated successfully"
    def post(self, request: Request, **kwargs):
        instance = self.call_service_method(self.create_service_method,
                                            self.get_object_id(),
                                            self.request.user)
        data = self.get_output_serializer_class()(instance).data
        return Response(
            {
                "success": True,
                "message": self.response_message,
                "data": data,
            }
        )


class BaseListCreateAPIView(BaseListAPIView, BaseCreateAPIView):
    pass


class BaseRetrieveAPIView(BaseCRUDAPIView):
    def get(self, request: Request, **kwargs):
        instance = self.call_service_method(self.retrieve_service_method,
                                            *self.get_retrieve_service_args(),
                                            **self.get_retrieve_service_kwargs())
        data = self.get_output_serializer_class()(instance).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name} retrieved successfully",
                "data": data,
            },
            status=status.HTTP_200_OK
        )


class BaseUpdateAPIView(BaseCRUDAPIView):
    def patch(self, request: Request, **kwargs):
        serializer = self.get_input_serializer_class()(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = self.call_service_method(self.update_service_method,
                                            *self.get_update_service_args(serializer),
                                            **self.get_update_service_kwargs(serializer))
        data = self.get_output_serializer_class()(instance).data
        return Response(
            {
                "success": True,
                "message": f"{self.resource_name} updated successfully",
                "data": data,
            },
            status=status.HTTP_200_OK
        )


class BaseRetrieveUpdateAPIView(BaseRetrieveAPIView, BaseUpdateAPIView):
    pass
