import uuid

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from common.models import CommonInfo

User = get_user_model()
    

class SocietyAmenities(CommonInfo):
    title = models.CharField(max_length=32)
    style_class = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = "property_society_amenities"

    def __str__(self):
        return self.title


class Gallery(CommonInfo):
    image = models.ImageField(upload_to="property/images")
    video = models.FileField(upload_to="property/videos")

    class Meta:
        db_table = "property_gallery"

    def __str__(self):
        return self.image


class Property(CommonInfo):
    MEMBERSHIP_PLAN_CHOICES = (
        ("S", "Silver"),
        ("G", "Gold"),
        ("P", "Platinum"),
    )
    LISTING_TYPE_CHOICES = (
        ("T", "Top"),
        ("P", "Premium"),
        ("F", "Featured"),
    )
    CONDITION_CHOICES = (
        ("N", "New"),
        ("U", "Used"),
    )
    PROPERTY_TYPE_CHOICES = (
        ("H", "House"),
        ("L", "Land"),
        ("F", "Flat"),
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
        ("D", "Don't Know")
    )
    DEVELOPMENT_PROGRESS_STATUS = (
        ("N", "Initial State"),
        ("I", "In Progress"),
        ("R", "Ready"),
    )
    COMMERCIAL_CHOICES = (
        ("R", "Rent"),
        ("S", "Sale"),
    )
    RESIDENTIAL_CHOICES = (
        ("R", "Rent"),
        ("S", "Resale"),
        ("P", "Pg/Hostel"),
        ("F", "Flatmates")
    )
    APARTMENT_CHOICES = (
        ("A", "Apartment"),
        ("I", "Independent House/Villa"),
        ("G", "Gated Community/Villa")
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
        ("20", "20")
    )
    AGE_CHOICES = (
        ("U", "Under Construction"),
        ("L", "Less than a year"),
        ("1", "1 to 3 year"),
        ("3", "3 to 5 year"),
        ("5", "5 to 10 year"),
        ("M", "More than 10 year")          
    )
    AVAILABLE_FOR_CHOICES = (
        ("R", "Only Rent"),
        ("L", "Only Lease")
    )
    MAINTENANCE_CHOICES = (
        ("I", "Maintenance Included"),
        ("E", "Maintenance Extra")
    )
    TENANTS_CHOICES = (
        ("D", "Doesn't Matter"),
        ("F", "Family"),
        ("B", "Bachelor"),
        ("C", "Company")
    )
    FURNISHING_CHOICES = (
        ("F", "Fully Furnishing"),
        ("S", "Semi Furnishing"),
        ("U", "Unfurnishing")
    )
    PARKING_CHOICES = (
        ("N", "None"),
        ("M", "Motorbike"),
        ("C", "Car"),
        ("B", "Both")
    )
    WATER_SUPPLY_CHOICES = (
        ("C", "Corporation"),
        ("W", "Borewell"),
        ("B", "Both")
    )
    YES_NO_CHOICES = (
        ("Y", "Yes"),
        ("N", "No")
    )
    VIEWER_CHOICES = (
        ("H", "Need Help"),
        ("I", "I will show"),
        ("N", "Neighbours"),
        ("F", "Friends/Relatives"),
        ("S", "Security"),
        ("T", "Tenants"),
        ("O", "Others")
    )
    AVAILABLE_DAY_CHOICES = (
        ("E", "Everyday(Sunday - Saturday)"),
        ("W", "Weekdays(Sunday - Friday)"),
        ("S", "Weekend(Saturday)")
    )
    owner = models.ForeignKey(User, related_name="properties", on_delete=models.CASCADE)
    agent = models.ForeignKey(
        User, related_name="agent_properties", on_delete=models.CASCADE
    )
    commercial = models.CharField(max_length=1, choices=COMMERCIAL_CHOICES, blank=True, null=True)
    residential = models.CharField(max_length=1, choices=RESIDENTIAL_CHOICES, blank=True, null=True)
    
    apartment_type = models.CharField(max_length=1, choices=APARTMENT_CHOICES, default="A")
    apartment_name = models.CharField(max_length=63, blank=True, null=True)
    bhk_type = models.IntegerField(default=0)# choice field
    floor = models.CharField(max_length=2, choices=NUMBER_OF_FLOOR_CHOICES, default="G")
    total_floor = models.CharField(max_length=2, choices=NUMBER_OF_FLOOR_CHOICES, default="G")# total floor
    property_age = models.CharField(max_length=1, choices=AGE_CHOICES, default="U")
    facing = models.CharField(max_length=2, choices=FACING_CHOICES)
    property_size = models.FloatField(default=0.00) #property size

    city = models.CharField(max_length=63, blank=True, null=True)
    locality = models.CharField(max_length=63)
    street_area = models.TextField()#street/area
    
    available_for = models.CharField(max_length=1, choices=AVAILABLE_FOR_CHOICES)
    expected_rent = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    expected_deposit = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    negotiable = models.BooleanField(default=False)
    maintenance = models.CharField(max_length=1, choices=MAINTENANCE_CHOICES, default="I")
    available_from = models.DateField()
    preferred_tenants = models.CharField(max_length=1, choices=TENANTS_CHOICES, default="D")
    furnishing = models.CharField(max_length=1, choices=FURNISHING_CHOICES, default="F")
    listing_type = models.CharField(max_length=1, choices=LISTING_TYPE_CHOICES, default="T")
    parking = models.CharField(max_length=1, choices=PARKING_CHOICES)
    description = models.TextField()
    
    gallery = models.ManyToManyField(Gallery, related_name="property_gallerys"
    )
    membership_plan = models.CharField(max_length=1, choices=MEMBERSHIP_PLAN_CHOICES,
                                       default="S")
    
    bathrooms = models.IntegerField(default=0)
    balcony = models.CharField(max_length=63, choices=YES_NO_CHOICES, default="Y")
    water_supply = models.CharField(max_length=1, choices=WATER_SUPPLY_CHOICES, default="C")
    gym = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    non_veg = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    gated_security = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    viewer = models.CharField(max_length=1, choices=VIEWER_CHOICES, default="H")
    secondary_number = models.IntegerField(default=1)

    paint = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    attached_bathroom = models.IntegerField(default=0)
    available_days = models.CharField(max_length=1, choices=AVAILABLE_DAY_CHOICES,default="E")
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    development_progress_status = models.CharField(
        max_length=1, choices=DEVELOPMENT_PROGRESS_STATUS, default="N"
    )
    
    land_area = models.FloatField(default=0.00)
    uid = models.UUIDField(unique=True, auto_created=True, null=True, blank=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    condition_type = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    #bedrooms = models.IntegerField(default=0)
    cleaned = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPE_CHOICES)
    furnished = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    viewed_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    society_amenities = models.ManyToManyField(
        SocietyAmenities, related_name="amenities",
    )
        
    location = models.PointField(null=True, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.property_type

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        if self.location:
            self.latitude = self.location.y
            self.longitude = self.location.x

        elif self.latitude and self.longitude:
            self.location = Point(x=self.longitude, y=self.latitude, srid=4326)

        super(Property, self).save(*args, **kwargs)

    class Meta:
        db_table = "property_property"
        get_latest_by = ["-membership_plan", "-added_at"]
        ordering = ["-membership_plan", "-added_at"]
        permissions = [("has_agent_permission", "Can Show Property")]

        indexes = [
            models.Index(fields=["city", "condition_type"]),
            models.Index(fields=["city", "commercial", "condition_type"]),
            models.Index(fields=["city", "residential", "condition_type"]),
            models.Index(fields=["storey"], name="storey_idx"),
            models.Index(fields=["parking"], name="parking_idx"),
            models.Index(fields=["facing"], name="facing_idx"),
        ]


class FieldVisit(CommonInfo):
    name = models.CharField(max_length=64, blank=False, null=False)
    email = models.CharField(max_length=16, blank=False)
    phone = models.CharField(max_length=16)
    property_type = models.ForeignKey(
        Property, related_name="field_visits", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        db_table = "property_field_visit"


class PropertyDiscussionBoard(CommonInfo):
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
    property_type = models.ForeignKey(
        Property, related_name="discussion", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "property_property_discussion"


class PropertyRequest(CommonInfo):
    REQUEST_CHOICES = (
        ("B", "Buy"),
        ("R", "Rent"),
        ("S", "Sell"),
    )
    PROPERTY_TYPE_CHOICES = (
        ("B", "House/Bungalow"),
        ("F", "Flat & Apartment"),
        ("C", "Commercial Property"),
        ("L", "Land"),
        ("A", "Agricultural Land"),
        ("O", "Office Space"),
        ("S", "Shutter & Shop Space"),
        ("R", "Restaurant for Sale"),
        ("H", "House in a Colony"),
    )
    URGENT_CHOICES = (
        ("V", "Very Urgent"),
        ("D", "Within a few days"),
        ("M", "Within a month"),
        ("F", "in few months time")
    )
    name = models.CharField(max_length=63)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    request_type = models.CharField(max_length=1, choices=REQUEST_CHOICES)
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPE_CHOICES)
    urgent = models.CharField(max_length=1, choices=URGENT_CHOICES)
    property_address = models.CharField(max_length=63)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    parking_space = models.FloatField()
    bedrooms = models.IntegerField(default=0)
    size = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "property_request"
        ordering = ["name"]