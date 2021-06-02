from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from itertools import chain
import django_filters.rest_framework
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView


from property.models import (
    ContactAgent,
    PropertyInfo,
    Gallery,
    FieldVisit,
    PropertyDiscussionBoard,
    RentalInfo,
    Amenities,
    Schedule,
    City,
    Location,
    PropertyRequest,
    FloorPlan,
)
from api.serializers.property_serializer import (
    PropertySerializer,
    FieldVisitSerializer,
    PropertyDiscussionSerializer,
    RentalSerializer,
    GallerySerializer,
    AmenitiesSerializer,
    ScheduleSerializer,
    LocationSerializer,
    PropertyDetailSerializer,
    CitySerializer,
    PropertyListingSerializer,
    DetailPropertySerializer,
    PropertyRequestSerializer,
    PropertyTypeFilteredSerialzers,
    ContactAgentSerializer,
    FloorPlanSerializer,
)


"""===================================
-- Property model on client side starts ---
======================================"""


class PropertyList(viewsets.ModelViewSet):
    """
    This views returns listing of property in client side
    """

    serializer_class = PropertyDetailSerializer
    queryset = PropertyInfo.objects.filter(publish=True)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        print("Obj", obj)
        obj.views = obj.views + 1
        obj.save(update_fields=("views",))
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=["GET"])
    def similar_property(self, request, pk=None):
        property_obj = self.get_object()
        similar_pro = PropertyInfo.objects.filter(
            property_type=property_obj.property_type, publish=True
        ).exclude(id=property_obj.id)
        serializer = self.get_serializer(similar_pro, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PropertyTop(generics.ListAPIView):
    """
    This views returns listing of top listing property
    """

    serializer_class = PropertyDetailSerializer

    def get_queryset(self):
        top_category = PropertyInfo.objects.filter(
            listing_type="T",
        ).filter(publish=True)
        return top_category


class PropertyPremium(generics.ListAPIView):
    """
    This views returns listing of premium property
    """

    serializer_class = PropertyDetailSerializer

    def get_queryset(self):
        premium_category = PropertyInfo.objects.filter(listing_type="P").filter(
            publish=True
        )
        return premium_category


class PropertyFeatured(generics.ListAPIView):
    """
    This views returns featured property
    """

    serializer_class = PropertyDetailSerializer

    def get_queryset(self):
        featured_category = PropertyInfo.objects.filter(listing_type="F").filter(
            publish=True
        )
        return featured_category


class PropertyFilterView(viewsets.ModelViewSet):
    """
    This views returns filtered property
    """

    queryset = PropertyInfo.objects.all()
    serializer_class = PropertyDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["price", "created_on"]
    search_fields = ["city", "bhk_type", "facing", "property_size", "property_adtype"]

    def get_queryset(self):
        verified_property = PropertyInfo.objects.filter(publish=True)
        city = self.request.query_params.get("city", None)
        bhk_type = self.request.query_params.get("bhk_type", None)
        print(bhk_type)
        facing = self.request.query_params.get("facing", None)
        property_size = self.request.query_params.get("property_size", None)
        property_adtype = self.request.query_params.get("property_adtype", None)
        if city:
            queryset = verified_property.filter(city__name=city)
            return queryset
        if bhk_type:
            queryset = verified_property.filter(bhk_type=bhk_type)
            return queryset
        elif facing:
            queryset = verified_property.filter(facing=facing)
            return queryset
        elif property_size:
            queryset = verified_property.filter(property_size=property_size)
            return queryset
        elif property_adtype:
            queryset = verified_property.filter(property_adtype=property_adtype)
            return queryset

        else:
            pass
        return super().get_queryset()


"""=========================================
----- Property model on admin side starts ---
============================================"""


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = PropertyInfo.objects.all()
    serializer_class = PropertySerializer


class RentalViewSet(viewsets.ModelViewSet):
    queryset = RentalInfo.objects.all()
    serializer_class = RentalSerializer
    filterset_fields = ["available_for", "tenants", "parking"]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        city_id = self.request.query_params.get("id", None)
        if city_id is not None:
            city = City.objects.get(id=city_id)
            queryset = Location.objects.select_related("city").filter(city=city.id)
            return queryset
        return super().get_queryset()


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class AmentitesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer


class FieldVisitViewSet(viewsets.ModelViewSet):
    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer
    filterset_fields = ["name", "email", "phone"]


class PropertyDiscussionViewSet(viewsets.ModelViewSet):
    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer
    filterset_fields = ["discussion"]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)


class PropertyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    This views returns detail of each property
    """

    queryset = PropertyInfo.objects.all()
    serializer_class = PropertyDetailSerializer


class PropertySearchView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["city", "locality"]


class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        city_name = self.request.query_params.get("name", None)
        print("city_name", city_name)
        if city_name is not None:
            city = City.objects.get(name=city_name)
            print("city", city)
            queryset = Location.objects.select_related("city").filter(city=city.id)
            return queryset
        return super().get_queryset()


class DetailPropertyView(generics.ListCreateAPIView):
    queryset = PropertyInfo.objects.all()
    serializer_class = DetailPropertySerializer


class PropertyRequestViewSet(viewsets.ModelViewSet):
    queryset = PropertyRequest.objects.all()
    serializer_class = PropertyRequestSerializer


class AdminDashboardView(APIView):
    def get(self, request):
        property_type_commercial = len(PropertyInfo.objects.filter(property_type="C"))
        property_type_residential = len(PropertyInfo.objects.filter(property_type="R"))

        # list of sellers,total property,buyers
        total_property = len(PropertyInfo.objects.filter(publish=True))
        sellers = len(PropertyInfo.objects.filter(publish=False))
        buyers = len(PropertyRequest.objects.all())

        data = [
            {
                "property_type_commercial": property_type_commercial,
                "property_type_residential": property_type_residential,
                "total_property": total_property,
                "sellers": sellers,
                "buyers": buyers,
            }
        ]
        results = PropertyTypeFilteredSerialzers(data, many=True).data
        return Response(results)


class ContactAgentViewSet(viewsets.ModelViewSet):
    queryset = ContactAgent.objects.all()
    serializer_class = ContactAgentSerializer


class FloorPlanViewSet(viewsets.ModelViewSet):
    queryset = FloorPlan.objects.all()
    serializer_class = FloorPlanSerializer
