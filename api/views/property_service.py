from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.property_service_serializer import PropertyServiceSerializer
from service_provider.models import ServiceProvider
from property.models import Property


class PropertyServiceDetailAPIView(APIView):

    serializer_class = PropertyServiceSerializer

    def get(self, request, *args, **kwargs):
        """
        Passing more than one queryset to the serializer
        """
        property_info = Property.objects.all()
        service_info = ServiceProvider.objects.all()
        qs_collection = {
            "property_info": property_info,
            "service_info": service_info,
        }
        serializer = self.serializer_class(qs_collection)
        return Response(serializer.data)
