from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers.serviceprovider_serializer import ServiceProviderSerializer, \
    ReviewSerializer, BusinessHourSerializer
from service_provider.models import ServiceProvider, Review, BusinessHours


class BusinessHourViewSet(viewsets.ModelViewSet):

    queryset = BusinessHours.objects.all()
    serializer_class = BusinessHourSerializer


class ServiceProviderViewSet(viewsets.ModelViewSet):

    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    filterset_fields = ["service_name", "address"]

    def get_queryset(self):
        params = self.request.query_params
        service_name = params.get("service_name")
        address = params.get("address")
        if service_name:
            self.queryset = self.queryset.filter(service_name=service_name)
        if address:
            self.queryset = self.queryset.filter(address=address)
        return self.queryset


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_fields = ["service_provider"]





