from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers.serviceprovider_serializer import ServiceProviderSerializer
from service_provider.models import ServiceProvider


class ServiceProviderViewSet(viewsets.ModelViewSet):

    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    filterset_fields = ["service_name", "location"]

    def get_queryset(self):
        params = self.request.query_params
        service_name = params.get("service_name")
        if service_name:
            self.queryset = self.queryset.filter(service_name=service_name)
        return self.queryset





