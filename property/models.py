from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from common.models import CommonInfo
from user.models import AdminProfile, UserProfile, AgentDetail, StaffDetail
from django.contrib.auth import get_user_model

User = get_user_model()


class City(CommonInfo):
    """model to store name of city"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "City"
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class PropertyCategories(CommonInfo):
    """model to store category of property"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"property category of {self.name}, {self.id}"

    class Meta:
        verbose_name_plural = "PropertyCategories"
        ordering = ["-created_on"]


class PropertyTypes(CommonInfo):
    """model to store type of property"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"property types of {self.name}, {self.id}"

    class Meta:
        verbose_name_plural = "PropertyTypes"
        ordering = ["-created_on"]


class Locality(CommonInfo):
    """model to locality details of property"""

    name = models.CharField(max_length=200)

    def __str__(self):
        return f"property types of {self.name}, {self.id}"

    class Meta:
        ordering = ["-created_on"]


class BasicDetails(CommonInfo):
    """
    model to store  basic details of the property
    """

    ADVERTISEMENT_TYPE_CHOICES = (
        ("", "----"),
        ("R", "Rent"),
        ("S", "Sale"),
    )
    MEMBERSHIP_PLAN_CHOICES = (
        ("S", "Silver"),
        ("G", "Gold"),
        ("P", "Platinum"),
    )
    LISTING_TYPE_CHOICES = (
        ("Fr", "Free"),
        ("P", "Premium"),
        ("Fe", "Featured"),
    )
    CONDITION_CHOICES = (
        ("N", "New"),
        ("U", "Used"),
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="city_property", null=True
    )
    property_categories = models.ForeignKey(
        PropertyCategories,
        on_delete=models.CASCADE,
        related_name="property_info",
        null=True,
        blank=True,
    )
    property_types = models.ForeignKey(
        PropertyTypes,
        on_delete=models.CASCADE,
        related_name="property_info",
        null=True,
        blank=True,
    )
    advertisement_type = models.CharField(
        max_length=2, choices=ADVERTISEMENT_TYPE_CHOICES, default=""
    )
    owner = models.ForeignKey(
        User,
        related_name="userprofile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    agent = models.ForeignKey(
        User,
        related_name="agentdetail",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    staff = models.ForeignKey(
        User,
        related_name="staffdetail",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    admin = models.ForeignKey(
        User,
        related_name="admin_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    publish = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    listing_type = models.CharField(
        max_length=2, choices=LISTING_TYPE_CHOICES, null=True, blank=True
    )
    membership_plan = models.CharField(
        max_length=1, choices=MEMBERSHIP_PLAN_CHOICES, null=True, blank=True
    )
    condition_type = models.CharField(
        max_length=1, choices=CONDITION_CHOICES, null=True, blank=True
    )  # sell type
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Basic Details"
        ordering = ["-created_on"]


"""=================================================
------------ Advertisement type Rent  ------------
====================================================="""


class RentPropertyDetails(CommonInfo):
    """
    Model to store the property details of rent type
    """

    BHK_CHOICES = (
        ("1 RK", "1 RK"),
        ("1 BHK", "1 BHK"),
        ("2 BHK", "2 BHK"),
        ("3 BHK", "3 BHK"),
        ("4 BHK", "4 BHK"),
        ("4+ BHK", "4+ BHK"),
    )
    FACING_CHOICES = (
        ("E", "EAST"),
        ("W", "WEST"),
        ("N", "North"),
        ("S", "South"),
        ("NE", "North-East"),
        ("SE", "South-East"),
        ("NW", "North-West"),
        ("SW", "South-West"),
        ("D", "Don't Know"),
    )
    basic_details = models.ForeignKey(
        BasicDetails, on_delete=models.CASCADE, related_name="rent_property", null=True
    )
    bhk_type = models.CharField(
        max_length=20, choices=BHK_CHOICES, default="F"
    )  # bedroom hall kitchen
    floor_number = models.CharField(max_length=40)
    total_floors = models.CharField(max_length=40)
    property_age = models.CharField(max_length=40)  # property age
    facing_direction = models.CharField(
        max_length=2, choices=FACING_CHOICES, default="E"
    )
    property_size = models.FloatField(default=0.00)  # size in sq.m

    def __str__(self):
        return f"property information of rent property with id {self.id}"

    class Meta:
        verbose_name_plural = "Rent Property Details"
        db_table = "rent_property_details"
        ordering = ["-created_on"]


class LocalityDetails(CommonInfo):
    """
    Locality details
    """

    basic_details = models.OneToOneField(
        BasicDetails, on_delete=models.CASCADE, related_name="location", null=True
    )
    locality = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name="location", null=True
    )
    street = models.TextField()
    # displaying the exact location using map
    location = models.PointField(blank=True, null=True)  # pin point location
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"property located at {self.id}"

    def save(self, *args, **kwargs):
        if self.location:
            self.latitude = self.location.y
            self.longitude = self.location.x

        elif self.latitude and self.longitude:
            self.location = Point(x=self.longitude, y=self.latitude, srid=4326)
        super(LocalityDetails, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Property Location"
        db_table = "property_location"
        ordering = ["-created_on"]


class RentalDetails(CommonInfo):
    """
    model to store the rental details of rent
    """

    PRICE_CHOICES = (("N", "Negotiable"), ("F", "Fixed"))
    FURNISHING_CHOICES = (
        ("F", "Fully Furnishing"),
        ("S", "Semi Furnishing"),
        ("U", "Unfurnishing"),
    )
    PARKING_CHOICES = (("N", "None"), ("M", "Motorbike"), ("C", "Car"), ("B", "Both"))
    basic_details = models.OneToOneField(
        BasicDetails, on_delete=models.CASCADE, related_name="rental_details", null=True
    )
    expected_rent = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    expected_deposit = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10, null=True, blank=True
    )
    price = models.CharField(max_length=1, choices=PRICE_CHOICES, default="N")

    available_from = models.DateField()
    furnishing = models.CharField(max_length=1, choices=FURNISHING_CHOICES, default="F")
    no_of_parking = models.CharField(max_length=1, choices=PARKING_CHOICES)
    description = models.TextField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Rental Info"
        db_table = "property_rental"
        ordering = ["-created_on"]


class Gallery(CommonInfo):
    """
    model to store the gallery
    """

    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="property/gallery")
    basic_details = models.OneToOneField(
        BasicDetails, on_delete=models.CASCADE, related_name="gallery", null=True
    )

    class Meta:
        verbose_name_plural = "Gallery"
        db_table = "Gallery"

    def __str__(self):
        # return str(self.id)
        return f"gallery {str(self.id)}"


"""=================================================
------------ Advertisement type Sale  ------------
====================================================="""


class SellPropertyDetails(CommonInfo):
    """
    model to store the sell property details
    """

    BHK_CHOICES = (
        ("1 RK", "1 RK"),
        ("1 BHK", "1 BHK"),
        ("2 BHK", "2 BHK"),
        ("3 BHK", "3 BHK"),
        ("4 BHK", "4 BHK"),
        ("4+ BHK", "4+ BHK"),
    )
    NUMBER_OF_FLOOR_CHOICES = (
        ("G", "Ground"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
        ("13", "13"),
        ("14", "14"),
        ("15", "15"),
        ("16", "16"),
        ("17", "17"),
        ("18", "18"),
        ("19", "19"),
        ("20", "20"),
    )
    AGE_CHOICES = (
        ("U", "Under Construction"),
        ("L", "Less than a year"),
        ("1", "1 to 3 year"),
        ("3", "3 to 5 year"),
        ("5", "5 to 10 year"),
        ("M", "More than 10 year"),
    )
    FACING_CHOICES = (
        ("E", "EAST"),
        ("W", "WEST"),
        ("N", "North"),
        ("S", "South"),
        ("NE", "North-East"),
        ("SE", "South-East"),
        ("NW", "North-West"),
        ("SW", "South-West"),
        ("D", "Don't Know"),
    )
    PROPERTY_SIZE_CHOICES = (("R", "Ropani"), ("A", "Aana"), ("S", "Square Feet"))
    basic_details = models.ForeignKey(
        BasicDetails,
        on_delete=models.CASCADE,
        related_name="sell_property_details",
        null=True,
    )
    bhk_type = models.CharField(
        max_length=20, choices=BHK_CHOICES, default="F"
    )  # bedroom hall kitchen
    total_floors = models.CharField(
        max_length=2, choices=NUMBER_OF_FLOOR_CHOICES, default="G"
    )
    property_age = models.CharField(
        max_length=1, choices=AGE_CHOICES, default="U"
    )  # property age
    built_up_area = models.DecimalField(
        default=0.00,
        decimal_places=2,
        max_digits=10,
    )
    property_size = models.DecimalField(
        default=0.00,
        decimal_places=2,
        max_digits=10,
    )
    facing_direction = models.CharField(max_length=2, choices=FACING_CHOICES)

    def __str__(self):
        return f"property information of sell property with id {self.id}"

    class Meta:
        verbose_name_plural = "SellPropertyDetails"
        ordering = ["-created_on"]


class ResaleDetails(CommonInfo):
    """
    This model defines the resale details of property.
    """

    PRICE_CHOICES = (("N", "Negotiable"), ("F", "Fixed"))
    FURNISHING_CHOICES = (
        ("F", "Fully Furnishing"),
        ("S", "Semi Furnishing"),
        ("U", "Unfurnishing"),
    )
    PARKING_CHOICES = (("N", "None"), ("M", "Motorbike"), ("C", "Car"), ("B", "Both"))
    KITCHEN_CHOICES = (
        ("F", "Fully furnished"),
        ("S", "Semi Furnishing"),
        ("U", "Unfurnished"),
    )
    CONSTRUCTION_CHOICES = (("C", "Completed"), ("N", "Not Completed"))

    expected_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    price = models.CharField(max_length=1, choices=PRICE_CHOICES, default="N")
    available_from = models.DateField()
    kitchen_type = models.CharField(max_length=1, choices=KITCHEN_CHOICES, default="F")
    furnishing = models.CharField(max_length=1, choices=FURNISHING_CHOICES, default="F")
    no_of_parking = models.CharField(max_length=1, choices=PARKING_CHOICES)
    construction_type = models.CharField(
        max_length=2, choices=CONSTRUCTION_CHOICES, default=""
    )
    pillar_size_width1 = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10
    )
    pillar_size_width2 = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10
    )
    description = models.TextField()
    basic_details = models.ForeignKey(
        BasicDetails, on_delete=models.CASCADE, related_name="resale_details", null=True
    )

    def __str__(self):
        return f"property resale details {self.id}"

    class Meta:
        verbose_name_plural = "ResaleDetails"
        ordering = ["-created_on"]


class Amenities(CommonInfo):
    """
    Amenities details of property.
    """

    basic_details = models.ForeignKey(
        BasicDetails, on_delete=models.CASCADE, related_name="amenities", null=True
    )
    total_no_bathrooms = models.IntegerField(default=0)
    water_supply = models.BooleanField(default=False)  # 24 hours hot water
    swimming_pool = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="sale/amenities")

    class Meta:
        verbose_name_plural = "Amenities"
        db_table = "property_amenities"

    def __str__(self):
        return str(self.id)


class FieldVisit(CommonInfo):
    """ "
    Visit made by buyer
    """

    name = models.CharField(max_length=64, blank=False, null=False)
    email = models.CharField(max_length=16, blank=False)
    phone = models.CharField(max_length=16)
    basic_details = models.ForeignKey(
        BasicDetails, on_delete=models.CASCADE, related_name="field_visit", null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Field Visit"
        ordering = ["-name"]
        db_table = "property_field_visit"


class PropertyDiscussionBoard(CommonInfo):
    """
    Property discussion board
    """

    DISCUSSION_CHOICES = (
        ("Q", "Query"),
        ("R", "Review"),
        ("S", "Suggestion"),
        ("C", "Complaint"),
    )
    discussion = models.CharField(max_length=1, choices=DISCUSSION_CHOICES)
    title = models.CharField(max_length=32, blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=32), blank=True)
    comments = models.TextField()
    basic_details = models.ForeignKey(
        BasicDetails,
        on_delete=models.CASCADE,
        related_name="discussion_board",
        null=True,
    )
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name="discussion_user",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title + " " + str(self.id)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Property Discussion Board"
        db_table = "property_discussionboard"


class Comment(CommonInfo):
    """This model defines the comment appeared on property discussion board"""

    user = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name="comment_user",
        blank=True,
        null=True,
    )
    discussion_board = models.ForeignKey(
        PropertyDiscussionBoard, on_delete=models.CASCADE, null=True
    )
    text = models.TextField(null=True)

    def __str__(self):
        return str(self.text)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Comment"


class Reply(CommonInfo):
    """Reply of the particular comment"""

    reply_madeby = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name="reply_madeby",
        blank=True,
        null=True,
        help_text="Reply made by user",
    )
    reply_madeto = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name="reply_madeto",
        blank=True,
        null=True,
        help_text="Reply done to specific user comment",
    )
    comment = models.ForeignKey(
        Comment, related_name="reply", on_delete=models.CASCADE, null=True
    )
    reply = models.TextField()

    def __str__(self):
        return str(self.id) + " " + self.reply

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Reply"


class PropertyRequest(CommonInfo):
    """
    This model refers to the request of property if someone wants to buy
    """

    REQUEST_TYPE_CHOICES = (
        ("B", "Buy"),
        ("R", "Rent"),
        ("S", "Sell"),
    )
    PROPERTY_TYPE_CHOICES = (
        ("B", "House/Bungalow"),
        ("F", "Flat & Apartment"),
        ("C", "Commercial Property"),
        ("L", "land"),
        ("A", "Agricultural Land"),
        ("O", "Office Space"),
        ("S", "Shutter & Shop Space"),
        ("R", "Restaurant for sale"),
        ("H", "House in a Colony"),
    )
    URGENT_CHOICES = (
        ("V", "Very Urgent"),
        ("W", "Within a few days"),
        ("M", "Within a month"),
        ("I", "In few months time"),
    )
    owner = models.ForeignKey(
        User,
        related_name="property_request_owner",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    agent = models.ForeignKey(
        User,
        related_name="property_request_agent",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    staff = models.ForeignKey(
        User,
        related_name="property_request_staff",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    request_type = models.CharField(max_length=1, choices=REQUEST_TYPE_CHOICES)
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPE_CHOICES)
    urgent = models.CharField(max_length=1, choices=URGENT_CHOICES)
    place = models.TextField()
    price_range = models.TextField()
    size = models.DecimalField(default=0.00, decimal_places=4, max_digits=10)
    due_date = models.DateField(null=True, blank=True)
    description_assigned_to_employee = models.TextField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Property Request"
        db_table = "property_request"


class ContactAgent(models.Model):
    """
    This model refers the contact of agent after someone wants a property
    """

    name = models.CharField(max_length=25, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    basic_details = models.ForeignKey(
        BasicDetails, on_delete=models.CASCADE, related_name="contact_agent", null=True
    )
    agent = models.ForeignKey(
        AgentDetail, on_delete=models.CASCADE, related_name="contact_agent"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Contact Agent"
