from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from common.models import CommonInfo
from user.models import AdminProfile, UserProfile, AgentDetail, StaffDetail
from django.contrib.auth import get_user_model

User = get_user_model()


class City(CommonInfo):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "City"
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class PropertyInfo(CommonInfo):
    """
    Info about property
    """

    APARTMENT_CHOICES = (
        ("Apartment", "Apartment"),
        ("Independent House/Villa", "Independent House/Villa"),
        ("Gated Community/Villa", "Gated Community/Villa"),
    )
    BHK_CHOICES = (
        ("1 RK", "1 RK"),
        ("1 BHK", "1 BHK"),
        ("2 BHK", "2 BHK"),
        ("3 BHK", "3 BHK"),
        ("4 BHK", "4 BHK"),
        ("4+ BHK", "4+ BHK"),
    )
    NUMBER_OF_FLOOR_CHOICES = (
        ("Ground", "Ground"),
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
        ("Under Construction", "Under Construction"),
        ("Less than a year", "Less than a year"),
        ("1 to 3 year", "1 to 3 year"),
        ("3 to 5 year", "3 to 5 year"),
        ("5 to 10 year", "5 to 10 year"),
        ("More than 10 year", "More than 10 year"),
    )
    FACING_CHOICES = (
        ("East", "East"),
        ("West", "West"),
        ("North", "North"),
        ("South", "South"),
        ("North-East", "North-East"),
        ("South-East", "South-East"),
        ("North-West", "North-West"),
        ("South-West", "South-West"),
        ("Don't Know", "Don't Know"),
    )
    PROPERTY_TYPE_CHOICES = (
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
    )
    PROPERTYAD_TYPE_CHOICES = (
        ("Rent", "Rent"),
        ("Resale", "Resale"),
        ("Pg/Hostel", "Pg/Hostel"),
        ("Flatmates", "Flatmates"),
        ("Sale", "Sale"),
    )
    MEMBERSHIP_PLAN_CHOICES = (
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
    )
    LISTING_TYPE_CHOICES = (
        ("Top", "Top"),
        ("Premium", "Premium"),
        ("Featured", "Featured"),
    )
    CONDITION_CHOICES = (
        ("New", "New"),
        ("Used", "Used"),
    )
    STATUS_CHOICES = (("Negotiation", "Negotiation"), ("P", "Pending"))

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="city_property", null=True
    )
    property_type = models.CharField(
        max_length=32, choices=PROPERTY_TYPE_CHOICES, default="Residential"
    )
    property_adtype = models.CharField(
        max_length=32, choices=PROPERTYAD_TYPE_CHOICES, default="R"
    )
    apartment_type = models.CharField(
        max_length=32, choices=APARTMENT_CHOICES, default="A"
    )
    apartment_name = models.CharField(max_length=63, blank=True, null=True)
    bhk_type = models.CharField(
        max_length=32, choices=BHK_CHOICES, default="F"
    )  # bedroom hall kitchen
    floor = models.CharField(max_length=32, choices=NUMBER_OF_FLOOR_CHOICES, default="G")
    total_floor = models.CharField(
        max_length=32, choices=NUMBER_OF_FLOOR_CHOICES, default="G"
    )
    age = models.CharField(
        max_length=32, choices=AGE_CHOICES, default="U"
    )  # property age
    facing = models.CharField(max_length=32, choices=FACING_CHOICES)
    property_size = models.FloatField(default=0.00)  # size in sq.m
    price = models.FloatField(default=0.00)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, null=True)
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

    # displaying the exact location using map
    location = models.PointField(null=True, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    listing_type = models.CharField(max_length=32, choices=LISTING_TYPE_CHOICES)
    membership_plan = models.CharField(max_length=32, choices=MEMBERSHIP_PLAN_CHOICES)
    condition_type = models.CharField(
        max_length=32, choices=CONDITION_CHOICES
    )  # sell type

    def __str__(self):
        return f"property information of {self.city}, with id {self.id}"

        return str(self.id)

    def save(self, *args, **kwargs):
        if self.location:
            self.latitude = self.location.y
            self.longitude = self.location.x

        elif self.latitude and self.longitude:
            self.location = Point(x=self.longitude, y=self.latitude, srid=4326)

        super(PropertyInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Property Info"
        db_table = "property"
        ordering = ["-created_on"]


class Location(CommonInfo):
    """
    Location of property
    """

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="city_locations", null=True
    )
    locality = models.TextField()
    street = models.TextField()
    listing = models.CharField(max_length=20, default="")
    property_info = models.OneToOneField(
        PropertyInfo, related_name="locations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"property located at {self.city}"

    class Meta:
        verbose_name_plural = "Property Location"
        db_table = "property_location"
        ordering = ["-created_on"]


class RentalInfo(CommonInfo):
    """
    rental details about property
    """

    AVAILABLE_FOR_CHOICES = (("Only Rent", "Only Rent"),
                             ("Only lease", "Only Lease"))
    MAINTENANCE_CHOICES = (("Maintenance Included", "Maintenance Included"),
                           ("Maintenance Extra", "Maintenance Extra"))
    TENANTS_CHOICES = (
        ("Doesn't Matter", "Doesn't Matter"),
        ("Family", "Family"),
        ("Bachelor", "Bachelor"),
        ("Company", "Company"),
    )
    FURNISHING_CHOICES = (
        ("Fully Furnishing", "Fully Furnishing"),
        ("Semi Furnishing", "Semi Furnishing"),
        ("Unfurnishing", "Unfurnishing"),
    )
    PARKING_CHOICES = (("None", "None"),
                       ("Motorbike", "Motorbike"),
                       ("Car", "Car"),
                       ("Both", "Both"))
    available_for = models.CharField(max_length=32, choices=AVAILABLE_FOR_CHOICES)
    expected_rent = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    expected_deposit = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10
    )
    negotiable = models.BooleanField(default=False)
    maintenance = models.CharField(
        max_length=32, choices=MAINTENANCE_CHOICES, default="I", blank=True, null=True
    )
    available_from = models.DateField()
    tenants = models.CharField(max_length=32, choices=TENANTS_CHOICES, default="D")
    furnishing = models.CharField(max_length=32, choices=FURNISHING_CHOICES, default="F")
    parking = models.CharField(max_length=32, choices=PARKING_CHOICES)
    description = models.TextField()
    property_info = models.ForeignKey(
        PropertyInfo, related_name="rental_info", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.available_for

    class Meta:
        verbose_name_plural = "Rental Info"
        db_table = "property_rental"
        ordering = ["-created_on"]


class Gallery(CommonInfo):
    """
    property info Gallery
    """

    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="property/images")
    property_info = models.ForeignKey(
        PropertyInfo, related_name="gallery", on_delete=models.CASCADE
    )
    link = models.URLField(max_length=400, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Gallery"
        db_table = "propertys_gallery"

    def __str__(self):
        # return str(self.id)
        return f"gallery {str(self.id)}"


class Amenities(CommonInfo):
    """
    Amenities
    """

    YES_NO_CHOICES = (("Yes", "Yes"), ("N0", "No"))
    WATER_SUPPLY_CHOICES = (("Corporation", "Corporation"),
                            ("Borewell", "Borewell"),
                            ("Both", "Both"))
    VIEWER_CHOICES = (
        ("Need Help", "Need Help"),
        ("I will show", "I will show"),
        ("Neighbours", "Neighbours"),
        ("Friends/Relatives", "Friends/Relatives"),
        ("Security", "Security"),
        ("Tenants", "Tenants"),
        ("Others", "Others"),
    )
    bathrooms = models.IntegerField(default=0)
    balcony = models.CharField(max_length=8, choices=YES_NO_CHOICES, default="Y")
    water_supply = models.CharField(
        max_length=32, choices=WATER_SUPPLY_CHOICES, default="C"
    )
    gym = models.CharField(max_length=32, choices=YES_NO_CHOICES, default="Y")
    non_veg = models.CharField(max_length=32, choices=YES_NO_CHOICES, default="Y")
    security = models.CharField(max_length=32, choices=YES_NO_CHOICES, default="Y")
    viewer = models.CharField(max_length=32, choices=VIEWER_CHOICES, default="H")
    secondary_number = models.IntegerField(default=1)
    property_info = models.ForeignKey(
        PropertyInfo, related_name="amenities", on_delete=models.CASCADE
    )

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
    property_type = models.ForeignKey(
        PropertyInfo, related_name="field_visits", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Field Visit"
        ordering = ["-name"]
        db_table = "property_field_visit"


class Schedule(models.Model):
    YES_NO_CHOICES = (("Yes", "Yes"), ("No", "No"))
    AVAILABLE_DAY_CHOICES = (
        ("Everyday(Sunday - Saturday", "Everyday(Sunday - Saturday)"),
        ("Weekdays(Sunday - Friday", "Weekdays(Sunday - Friday)"),
        ("Weekend(Saturday)", "Weekend(Saturday)"),
    )

    paint = models.CharField(
        max_length=8, choices=YES_NO_CHOICES, default="Y", null=True, blank=True
    )  # i want my house painted
    cleaned = models.CharField(
        max_length=8, choices=YES_NO_CHOICES, default="Y", null=True, blank=True
    )  # i want to get my house cleaned
    available_days = models.CharField(
        max_length=32, choices=AVAILABLE_DAY_CHOICES, default="E", null=True, blank=True
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    property_type = models.ForeignKey(
        PropertyInfo, related_name="property_schedule", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Schedule"
        db_table = "property_schedule"

    def __str__(self):
        return self.paint


class PropertyDiscussionBoard(CommonInfo):
    """
    Property discussion board
    """

    DISCUSSION_CHOICES = (
        ("Query", "Query"),
        ("Review", "Review"),
        ("Suggestion", "Suggestion"),
        ("Complaint", "Complaint"),
    )
    discussion = models.CharField(max_length=32, choices=DISCUSSION_CHOICES)
    title = models.CharField(max_length=32, blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=32), blank=True)
    comments = models.TextField()
    property_type = models.ForeignKey(
        PropertyInfo, related_name="discussion", on_delete=models.CASCADE
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
        ("Buy", "Buy"),
        ("Rent", "Rent"),
        ("Sell", "Sell"),
    )
    PROPERTY_TYPE_CHOICES = (
        ("House/Bungalow", "House/Bungalow"),
        ("Flat & Apartment", "Flat & Apartment"),
        ("Commercial Property", "Commercial Property"),
        ("Land", "Land"),
        ("Agricultural Land", "Agricultural Land"),
        ("Office Space", "Office Space"),
        ("Shutter & Shop Space", "Shutter & Shop Space"),
        ("Restaurant for Sale", "Restaurant for sale"),
        ("House in a Colony", "House in a Colony"),
    )
    URGENT_CHOICES = (
        ("Very Urgent", "Very Urgent"),
        ("Within a few days", "Within a few days"),
        ("Within a month", "Within a month"),
        ("In few months time", "In few months time"),
    )
    name = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    request_type = models.CharField(max_length=32, choices=REQUEST_TYPE_CHOICES)
    property_type = models.CharField(max_length=32, choices=PROPERTY_TYPE_CHOICES)
    urgent = models.CharField(max_length=32, choices=URGENT_CHOICES)
    place = models.TextField()
    price_range = models.TextField()
    size = models.DecimalField(default=0.00, decimal_places=4, max_digits=10)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Property Request"
        db_table = "property_request"


class FloorPlan(CommonInfo):
    """
    This model includes the architecture of property including map
    """

    property_type = models.ForeignKey(
        PropertyInfo, related_name="floor_plan", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=40, blank=True, null=True)
    file = models.FileField(upload_to="floorplan/images", null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Floorplan"
        db_table = "Floor plan"


class ContactAgent(models.Model):
    """
    This model refers the contact of agent after someone wants a property
    """

    name = models.CharField(max_length=25, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    property_info = models.ForeignKey(
        PropertyInfo, on_delete=models.CASCADE, related_name="property_info"
    )
    agent = models.ForeignKey(
        AgentDetail, on_delete=models.CASCADE, related_name="agent"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Contact Agent"
