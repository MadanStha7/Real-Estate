from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from itertools import chain
from datetime import datetime, timezone
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from user.models import AgentDetail, UserProfile, AdminProfile
from django.contrib.auth.models import Group

from api.permissions.user_permission import (
    UserIsAuthenticated,
    UserIsAdmin,
    UserIsStaffDetail,
    UserIsBuyerOrSeller,
    UserIsAgentDetail,
)
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
    Comment,
    Reply,
    PropertyCategories,
    PropertyTypes,
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
    CommentSerializer,
    ReplySerializer,
    PropertyCategoriesSerializer,
    PropertyTypeSerializer,
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

    @action(detail=True, methods=["GET"])
    def get_gallery(self, request):
        property = PropertyInfo.objects.get(id=self.id)
        gallery = Gallery.objects.filter(property_info=property.id)
        return gallery


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

        # for both city and locality

        else:
            pass
        return super().get_queryset()


"""=========================================
----- Property model on admin side starts ---
============================================"""


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = PropertyInfo.objects.all()
    serializer_class = PropertySerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        get_group = self.request.user.groups.all()
        for group in get_group:
            if group.name == "BuyerOrSeller":
                owner = self.request.user
                admin = None
            elif group.name == "Admin":
                admin = self.request.user
                owner = None
            else:
                pass
        serializer.save(owner=owner, admin=admin)

    @action(detail=False, methods=["GET"])
    def verify_property(self, request):
        property = self.request.query_params.get("property", None)
        if property:
            get_property = PropertyInfo.objects.get(id=property)
            get_property.publish = True
            get_property.save()
            return Response(
                {"message": "property successfully verified"}, status=status.HTTP_200_OK
            )

        else:
            raise ValidationError({"error": "property is required"})

    @action(detail=False, methods=["GET"])
    def listing_type(self, request):
        """get the property and save as if it is top,premium,or featured"""
        property = self.request.query_params.get("property", None)
        property_listing_type = self.request.query_params.get("listing_type", None)
        if property and property_listing_type:
            get_property = PropertyInfo.objects.get(id=property, publish=True)
            get_property.listing_type = property_listing_type
            get_property.save()
            return Response(
                {"message": "Data successfully submitted"}, status=status.HTTP_200_OK
            )

        else:
            raise ValidationError({"error": "property is required"})


class RentalViewSet(viewsets.ModelViewSet):
    queryset = RentalInfo.objects.all()
    serializer_class = RentalSerializer
    filterset_fields = ["available_for", "tenants", "parking"]

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        city_id = self.request.query_params.get("id", None)
        city = self.request.query_params.get("city", None)
        locality = self.request.query_params.get("locality", None)
        print("locality", locality)
        print("city", city)

        # for admin purposes to display all locations based on the cities
        if city_id is not None:
            city = City.objects.get(id=city_id)
            queryset = Location.objects.select_related("city").filter(city=city.id)
            return queryset

        # for client side search
        if (city and locality) is not None:
            try:
                city_name = City.objects.get(name=city)
                try:
                    queryset = Location.objects.filter(
                        city=city_name.id, locality__icontains=locality
                    )
                    return queryset
                except Location.DoesNotExist:
                    raise ValidationError(
                        {"error": "Location with this city name doesn't exist"}
                    )

            except City.DoesNotExist:
                raise ValidationError({"error": "City doesn't exist"})

        if city is not None:
            try:
                city = City.objects.get(name=city)
                try:
                    queryset = Location.objects.select_related("city").filter(
                        city=city.id
                    )
                except Location.DoesNotExist:
                    raise ValidationError(
                        {"error": "Location with this city name doesn't have"}
                    )
            except City.DoesNotExist:
                raise ValidationError({"error": "City doesn't exist"})
            return queryset

        if locality is not None:
            try:
                queryset = Location.objects.filter(locality__icontains=locality)
                return queryset
            except Location.DoesNotExist:
                raise ValidationError({"error": "Location doesn't exist"})
        return super().get_queryset()


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class AmentitesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class FieldVisitViewSet(viewsets.ModelViewSet):
    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer
    filterset_fields = ["name", "email", "phone"]

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PropertyDiscussionViewSet(viewsets.ModelViewSet):
    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer
    filterset_fields = ["discussion"]

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=["GET"])
    def total_discussion(self, request, pk=None):
        """Total number of comments in a single property"""
        property_obj = self.get_object()
        discussion = PropertyDiscussionBoard.objects.select_related(
            "property_type"
        ).filter(property_type=property_obj.id)
        # return queryset
        serializer = self.get_serializer(discussion, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

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

    # for homepage city and locality search


class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class DetailPropertyView(generics.ListCreateAPIView):
    queryset = PropertyInfo.objects.all()
    serializer_class = DetailPropertySerializer


class PropertyRequestViewSet(viewsets.ModelViewSet):
    queryset = PropertyRequest.objects.all()
    serializer_class = PropertyRequestSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


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

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class FloorPlanViewSet(viewsets.ModelViewSet):
    queryset = FloorPlan.objects.all()
    serializer_class = FloorPlanSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    """This view shows the comment on discussion board"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=["GET"])
    def total_discussion(self, request, pk=None):
        """Total number of comments in a single property"""
        property_obj = get_object_or_404(PropertyInfo.objects.filter(id=pk))
        if property_obj is not None:
            try:
                comment = Comment.objects.filter(
                    discussion_board__property_type__id=property_obj.id
                )
                print("comment", comment)
                serializer = self.get_serializer(comment, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Comment.DoesNotExist:
                raise ValidationError({"error": "No data to display"})
        else:
            return Response({"data": "No data to display"}, status=status.HTTP_200_OK)


class ReplyViewSet(viewsets.ModelViewSet):
    """This view shows the reply on comment"""

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PropertyCategoryViewset(viewsets.ModelViewSet):
    queryset = PropertyCategories.objects.all()
    serializer_class = PropertyCategoriesSerializer


class PropertyTypesViewSet(viewsets.ModelViewSet):
    queryset = PropertyTypes.objects.all()
    serializer_class = PropertyTypeSerializer


class PropertyCategoriesFilterViewSet(viewsets.ModelViewSet):
    queryset = PropertyInfo.objects.all()
    serializer_class = PropertyDetailSerializer

    def get_queryset(self):
        property_categories_id = self.request.query_params.get("id", None)
        property_categories_name = self.request.query_params.get("name", None)

        if property_categories_id is not None:
            property_categories = PropertyCategories.objects.get(
                id=property_categories_id
            )
            queryset = PropertyInfo.objects.select_related(
                "property_categories"
            ).filter(property_categories=property_categories.id)
            return queryset

        if property_categories_name is not None:
            property_categories = PropertyCategories.objects.get(
                name=property_categories_name
            )
            queryset = PropertyInfo.objects.select_related(
                "property_categories"
            ).filter(property_categories=property_categories.id)
            return queryset

        return super().get_queryset()


class PropertyTypesFilterViewSet(viewsets.ModelViewSet):
    queryset = PropertyInfo.objects.all()
    serializer_class = PropertyDetailSerializer

    def get_queryset(self):
        property_types_id = self.request.query_params.get("id", None)
        property_types_name = self.request.query_params.get("name", None)

        if property_types_id is not None:
            property_types = PropertyTypes.objects.get(id=property_types_id)
            queryset = PropertyInfo.objects.select_related("property_types").filter(
                property_types=property_types.id
            )
            return queryset

        if property_types_name is not None:
            property_types = PropertyTypes.objects.get(name=property_types_name)
            queryset = PropertyInfo.objects.select_related("property_types").filter(
                property_types=property_types.id
            )
            return queryset

        return super().get_queryset()
