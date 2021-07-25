from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from itertools import chain
from datetime import datetime, timezone
from rest_framework import filters
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from user.models import AgentDetail, UserProfile, AdminProfile
from api.permissions.user_permission import (
    UserIsAuthenticated,
    UserIsAdmin,
    UserIsStaffDetail,
    UserIsBuyerOrSeller,
    UserIsAgentDetail,
)
from property.models import (
    City,
    PropertyCategories,
    Locality,
    PropertyTypes,
    BasicDetails,
    RentPropertyDetails,
    Gallery,
    SellPropertyDetails,
    ResaleDetails,
    Amenities,
    FieldVisit,
    PropertyDiscussionBoard,
    PropertyRequest,
    ContactAgent,
    Comment,
    Reply,
    RentalDetails,
    LocalityDetails,
    FloorPlan,
)
from api.serializers.property_serializer import (
    AmenitiesSerializer,
    BasicDetailsSerializer,
    CitySerializer,
    LocalityDetailsSerializer,
    LocalitySerializer,
    # LocationSerializer,
    PropertyCategoriesSerializer,
    PropertyTypeSerializer,
    RentPropertyDetailsSerializer,
    RentalDetailsSerializer,
    PendingPropertySerializer,
    AssignPropertySerializer,
    ResaleDetailsSerializer,
    SellPropertyDetailsSerializer,
    FieldVisitSerializer,
    DashBoardSerialzer,
    PropertyRequestSerializer,
    GallerySerializer,
    PropertyDiscussionSerializer,
    AssignPropertyRequestSerializer,
    FloorPlanSerializer,
    BasicDetailRetrieveSerializer,
    CommentSerializer,
    ReplySerializer,
    SuggestionSerializer,
    BasicDetailListSerializer,
)
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


"""===================================
-- Property model on client side starts ---
======================================"""


class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class ListedPropertyViewSet(viewsets.ModelViewSet):
    queryset = BasicDetails.objects.filter(publish=True)
    serializer_class = BasicDetailsSerializer


class PremiumPropetyViewSet(generics.ListAPIView):
    serializer_class = BasicDetailRetrieveSerializer

    def get_queryset(self):
        premium_category = BasicDetails.objects.filter(listing_type="P").filter(
            publish=True
        )
        return premium_category


class FeaturedPropetyViewSet(generics.ListAPIView):
    serializer_class = BasicDetailRetrieveSerializer

    def get_queryset(self):
        featured_category = BasicDetails.objects.filter(listing_type="Fe").filter(
            publish=True
        )
        return featured_category


class FreePropetyViewSet(generics.ListAPIView):
    serializer_class = BasicDetailRetrieveSerializer

    def get_queryset(self):
        free_category = BasicDetails.objects.filter(listing_type="Fr").filter(
            publish=True
        )
        return free_category


class PropertyFilter(viewsets.ModelViewSet):
    """
    This views returns property on the basis of filterations.
    """

    queryset = BasicDetails.objects.none()
    serializer_class = BasicDetailRetrieveSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["property_categories", "property_types", "city"]

    def get_queryset(self):
        verified_property = BasicDetails.objects.filter(publish=True)
        property_categories = self.request.query_params.get("property_categories", None)
        property_types = self.request.query_params.get("property_types", None)
        city = self.request.query_params.get("city", None)

        if property_categories and city and property_types:
            queryset = verified_property.filter(
                property_categories__name=property_categories,
                city__name=city,
                property_types__name=property_types,
            )
            return queryset
        elif property_categories and city:
            queryset = verified_property.filter(
                property_categories__name=property_categories, city__name=city
            )
            return queryset
        elif property_categories and property_types:
            queryset = verified_property.filter(
                property_categories__name=property_categories,
                property_types__name=property_types,
            )
            return queryset
        elif city and property_types:
            queryset = verified_property.filter(
                property_types__name=property_types, city__name=city
            )
            return queryset
        elif property_categories:
            queryset = verified_property.filter(
                property_categories__name=property_categories
            )
            return queryset

        elif property_types:
            queryset = verified_property.filter(property_types__name=property_types)
            return queryset
        elif city:
            queryset = verified_property.filter(city__name=city)
            return queryset
        else:
            return BasicDetails.objects.filter(publish=True)


class PropertySearchViewSet(viewsets.ModelViewSet):
    queryset = BasicDetails.objects.all()
    serializer_class = BasicDetailRetrieveSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["advertisement_type"]
    search_fields = ["city", "locality"]

    def get_queryset(self):
        verified_property = BasicDetails.objects.filter(publish=True)
        city = self.request.query_params.get("city", None)
        locality = self.request.query_params.get("locality", None)
        # advertisement_type = self.request.query_params.get("advertisement_type", None)
        if city:
            queryset = verified_property.filter(city__name=city)
            return queryset
        if locality:
            queryset = verified_property.filter(location__locality__name=locality)
            return queryset
        # if advertisement_type:
        #     queryset = verified_property.filter(advertisement_type=advertisement_type)
        #     return queryset
        else:
            return BasicDetails.objects.filter(publish=True)


class PropertyFilterView(viewsets.ModelViewSet):
    """
    This views returns filtered property
    """

    queryset = BasicDetails.objects.all()
    serializer_class = BasicDetailRetrieveSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["advertisement_type"]
    ordering_fields = ["created_on"]
    search_fields = [
        "city",
        "bhk_type",
        "facing_direction",
        "property_age",
    ]

    def get_queryset(self):
        verified_property = BasicDetails.objects.filter(publish=True)
        city = self.request.query_params.get("city", None)
        bhk_type = self.request.query_params.get("bhk_type", None)
        facing_direction = self.request.query_params.get("facing_direction", None)
        property_age = self.request.query_params.get("property_age", None)
        if city:
            queryset = verified_property.filter(city__name=city)
            return queryset
        if bhk_type:
            queryset = verified_property.filter(
                sell_property_details__bhk_type=bhk_type
            ) | verified_property.filter(rent_property__bhk_type=bhk_type)
            return queryset
        if facing_direction:
            queryset = verified_property.filter(
                sell_property_details__facing_direction=facing_direction
            ) | verified_property.filter(
                rent_property__facing_direction=facing_direction
            )
            return queryset
        elif property_age:
            queryset = verified_property.filter(
                sell_property_details__property_age=property_age
            ) | verified_property.filter(rent_property__property_age=property_age)
            return queryset

        else:
            pass
        return super().get_queryset()


class PropertyTypesViewSet(viewsets.ModelViewSet):
    queryset = PropertyTypes.objects.all()
    serializer_class = PropertyTypeSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PropertyCategoryViewset(viewsets.ModelViewSet):
    queryset = PropertyCategories.objects.all()
    serializer_class = PropertyCategoriesSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class LocalityViewset(viewsets.ModelViewSet):
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class BasicDetailsViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the basic details of both rent and sale
    """

    queryset = BasicDetails.objects.all()
    serializer_class = BasicDetailsSerializer
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    # def perform_create(self, serializer):
    #     get_group = self.request.user.groups.all()

    #     for group in get_group:
    #         if group.name == "BuyerOrSeller":
    #             users = self.request.user
    #             posted_by= users.buyer_seller_profile.full_name
    #         elif group.name == "Admin":
    #             admin = self.request.user
    #             owner = None
    #         else:
    #             pass
    #     serializer.save(posted_by= posted_by)

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy", "approve_property"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]
        if self.action in ["approve_property"]:
            return [IsAuthenticated(), UserIsAdmin()]
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=["GET"])
    def approve_property(self, request):
        property = self.request.query_params.get("property_id", None)
        if property:
            get_property = BasicDetails.objects.get(id=property)
            get_property.publish = True
            get_property.save()
            return Response(
                {"message": "property successfully approved"}, status=status.HTTP_200_OK
            )

        else:
            raise ValidationError({"error": "property is required"})

    @action(detail=False, methods=["get"], url_path="similar-property")
    def similar_property(self, request, *args, **kwargs):
        property = self.request.query_params.get("property_id", None)
        if property:
            try:
                basic_details = BasicDetails.objects.get(id=property, publish=True)
                similar_property = BasicDetails.objects.filter(
                    advertisement_type=basic_details.advertisement_type,
                    publish=True,
                    property_categories=basic_details.property_categories,
                    property_types=basic_details.property_types,
                    city=basic_details.city,
                ).order_by("-id")[:4]
                serializer = BasicDetailRetrieveSerializer(similar_property, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BasicDetails.DoesNotExist:
                raise ValidationError(
                    {"error": "Object with this property id doesn't exist!"}
                )
        else:
            raise ValidationError({"error": "property is required"})

    @action(detail=False, methods=["get"], url_path="property-price-list")
    def property_price_list_display(self, request, *args, **kwargs):
        """"api to filter the price list from low to high"""
        low_to_high = self.request.query_params.get("low_to_high", None)
        high_to_low = self.request.query_params.get("high_to_low", None)

        # get the price from both rental details and resale details
        rental_details = RentalDetails.objects.filter(
            basic_details__publish=True
        ).values("expected_rent")
        resale_details = ResaleDetails.objects.filter(
            basic_details__publish=True
        ).values("expected_price")

        price_list = []
        for price in rental_details:
            price_list.append(price["expected_rent"])

        for price in resale_details:
            price_list.append(price["expected_price"])

        # sorted in ascending order
        if low_to_high:
            price_data = sorted(price_list, key=lambda x: float(x))
        # sorted in descending order
        if high_to_low:
            price_data = sorted(price_list, key=lambda x: float(x), reverse=True)

        # get all the data of rental and resale details
        overall_data = []
        for price in price_data:
            all_price_rent = RentalDetails.objects.filter(
                basic_details__publish=True, expected_rent=price
            )
            if all_price_rent:
                overall_data.append(all_price_rent)
            else:
                all_price_resale = ResaleDetails.objects.filter(
                    basic_details__publish=True, expected_price=price
                )
                overall_data.append(all_price_resale)

        # get all the data in basic detail serialzers
        main_data = []
        for element in overall_data:
            for item in element:
                try:
                    basic_details = BasicDetails.objects.get(id=item.basic_details.id)
                except BasicDetails.DoesNotExist:
                    pass
                results = BasicDetailsSerializer(basic_details).data
                main_data.append(results)
        return Response(main_data, status=status.HTTP_200_OK)


class RentPropertyDetailsViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the basic details of both rent and sale
    """

    queryset = RentPropertyDetails.objects.all()
    serializer_class = RentPropertyDetailsSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class LocalityDetailsViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the basic details of both rent and sale
    """

    queryset = LocalityDetails.objects.all()
    serializer_class = LocalityDetailsSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class RentalDetailsViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the basic rental details
    """

    queryset = RentalDetails.objects.all()
    serializer_class = RentalDetailsSerializer
    pagination_class = None


class SellPropertyDetailsViewSet(viewsets.ModelViewSet):
    queryset = SellPropertyDetails.objects.all()
    serializer_class = SellPropertyDetailsSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class GalleryViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the rent gallery
    """

    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    pagination_class = None


class ResaleDetailsViewSet(viewsets.ModelViewSet):
    queryset = ResaleDetails.objects.all()
    serializer_class = ResaleDetailsSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PendingPropertyViewset(viewsets.ModelViewSet):
    """
    Viewsets to display the pending property
    """

    queryset = BasicDetails.objects.none()
    serializer_class = PendingPropertySerializer
    pagination_class = None

    def get_queryset(self):
        advertisement_type = self.request.query_params.get("advertisement_type", False)
        if advertisement_type == "rent":
            queryset = BasicDetails.objects.filter(
                advertisement_type="R", publish=False
            )
            return queryset
        if advertisement_type == "sale":
            queryset = BasicDetails.objects.filter(
                advertisement_type="S", publish=False
            )
            return queryset
        else:
            queryset = BasicDetails.objects.filter(publish=False)
            return queryset


class AmenitiesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class AssignPropertyViewset(generics.CreateAPIView):
    """Api to assign the property to employee"""

    queryset = BasicDetails.objects.filter(publish=False)
    serializer_class = AssignPropertySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        pending_property = self.request.query_params.get("pending_property_id", False)
        try:
            basic_details = BasicDetails.objects.get(id=pending_property)
        except BasicDetails.DoesNotExist:
            raise ValidationError({"error": "basic details doesn't exist"})
        staff = self.request.data.get("staff")
        due_date = self.request.data.get("due_date")
        description = self.request.data.get("description")
        basic_details.staff = User.objects.get(id=staff)
        basic_details.due_date = due_date
        basic_details.description = description
        basic_details.save()


class FieldVisitViewSet(viewsets.ModelViewSet):
    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer
    filterset_fields = ["name", "email", "phone"]


class DashBoardView(APIView):
    def get(self, request, *args, **kwargs):
        listed_property = len(BasicDetails.objects.filter(publish=True))
        sellers = len(BasicDetails.objects.all())
        buyers = len(PropertyRequest.objects.all())
        agents = len(AgentDetail.objects.all())
        property_type_commercial = len(
            BasicDetails.objects.filter(property_types__name="commercial")
        )
        property_type_residential = len(
            BasicDetails.objects.filter(property_types__name="residential")
        )
        data = [
            {
                "listed_property": listed_property,
                "sellers": sellers,
                "buyers": buyers,
                "agents": agents,
                "property_type_commercial": property_type_commercial,
                "property_type_residential": property_type_residential,
                # "rental": rental,
                # "resale": resale,
            }
        ]
        results = DashBoardSerialzer(data, many=True).data
        return Response(results)


class DashBoardPendingPropertyView(APIView):
    """API to list all pending property in home section dashboard """

    def get(self, request):
        basic_details = BasicDetails.objects.filter(publish=False).order_by("-id")[:5]
        pending_property = []
        for element in basic_details:
            if element.property_types:
                property_type = element.property_types.name
            else:
                property_type = None

            if element.property_categories:
                property_categories = element.property_categories.name
            else:
                property_categories = None

            if element.advertisement_type:
                advertisement_type = element.get_advertisement_type_display()
            else:
                advertisement_type = None

            location = LocalityDetails.objects.filter(
                basic_details__id=element.id
            ).values("locality__name")
            rental_details_price = RentalDetails.objects.filter(
                basic_details__id=element.id
            ).values("expected_rent")

            resale_details_price = ResaleDetails.objects.filter(
                basic_details__id=element.id
            ).values("expected_price")
            print("resale_details_price", resale_details_price)

            pending_property.append(
                {
                    "property_type": property_type,
                    "property_categories": property_categories,
                    "advertisement_type": advertisement_type,
                    "location": location,
                    "rental_details_price": rental_details_price,
                    "resale_details_price": resale_details_price,
                }
            )
        return Response(pending_property)


class PropertyRequestViewSet(viewsets.ModelViewSet):
    queryset = PropertyRequest.objects.all()
    serializer_class = PropertyRequestSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PropertyDiscussionViewSet(viewsets.ModelViewSet):
    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "finish"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class AssignPropertyRequestViewset(generics.CreateAPIView):
    """Api to assign the propertyrequest to employee"""

    queryset = PropertyRequest.objects.all()
    serializer_class = AssignPropertyRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_request = self.request.query_params.get("property_request_id", False)
        print("property_request")
        try:
            property_request_obj = PropertyRequest.objects.get(id=property_request)
        except BasicDetails.DoesNotExist:
            raise ValidationError({"error": "Property Request doesn't exist"})
        staff = self.request.data.get("staff")
        due_date = self.request.data.get("due_date")
        description_assigned_to_employee = self.request.data.get(
            "description_assigned_to_employee"
        )
        property_request_obj.staff = User.objects.get(id=staff)
        property_request_obj.due_date = due_date
        property_request_obj.description_assigned_to_employee = (
            description_assigned_to_employee
        )
        property_request_obj.save()


class FloorPlanViewset(viewsets.ModelViewSet):
    """API for floorplan"""

    queryset = FloorPlan.objects.all()
    serializer_class = FloorPlanSerializer


class BasicDetailRetrieveView(generics.RetrieveAPIView):
    """API to retrieve the single basic detail in client detail page"""

    queryset = BasicDetails.objects.filter(publish=True)
    serializer_class = BasicDetailRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        """API to count the number of views in property"""
        obj = self.get_object()
        print("Obj", obj)
        obj.views = obj.views + 1
        obj.save(update_fields=("views",))
        return super().retrieve(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """This view shows the comment on discussion board"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=["GET"])
    def total_discussion(self, request, pk=None):
        """Total number of comments in a single property"""
        property_obj = get_object_or_404(BasicDetails.objects.filter(id=pk))
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

        # property_obj = self.get_object()


class ReplyViewSet(viewsets.ModelViewSet):
    """This view shows the reply on comment"""

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class NameSuggestions(APIView):
    """
    api for locality suggestions during search
    """

    queryset = None
    serializer_class = SuggestionSerializer

    def get(self, request, *args, **kwargs):
        city = self.request.query_params.get("city", "")
        name = self.request.query_params.get("name", "")
        name_suggestions = []
        if name:
            localitys = Locality.objects.filter(city__name=city).values("name")
            for locality in localitys:
                if name.lower() in locality.get("name", "").lower():
                    name_suggestions.append(locality.get("name"))
        res = {"suggestions": list(set(name_suggestions))}

        return Response(res)


class LocalityFilter(APIView):
    """
    API to return the locality of specific city
    """

    queryset = None
    serializer_class = None

    def get(self, request, *args, **kwargs):
        city = self.request.query_params.get("city", "")
        if city:
            localitys = Locality.objects.filter(city__name=city).values("id", "name")
            return Response(localitys)


class PendingPropertyListview(generics.ListAPIView):
    """API to displays list of pending property"""

    queryset = BasicDetails.objects.filter(publish=False)
    serializer_class = BasicDetailListSerializer


class ListedPropertyListview(generics.ListAPIView):
    """API to displays list of listed property"""

    queryset = BasicDetails.objects.filter(publish=False)
    serializer_class = BasicDetailListSerializer


class MyPropertyViewset(viewsets.ModelViewSet):
    """
    Viewsets to show property of login user
    """

    queryset = BasicDetails.objects.all()
    serializer_class = BasicDetailRetrieveSerializer

    def get_queryset(self):
        queryset = BasicDetails.objects.filter(posted_by=self.request.user.id)
        if queryset is not None:
            return queryset
        else:
            return Response({"message": "Please login to view profile."})
