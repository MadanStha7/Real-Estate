from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from common.models import CommonInfo
from user.models import UserProfile, AgentDetail, StaffDetail


class RentalInfo(CommonInfo):
    """
    rental details about property
    """

    AVAILABLE_FOR_CHOICES = (("R", "Only Rent"), ("L", "Only Lease"))
    MAINTENANCE_CHOICES = (("I", "Maintenance Included"), ("E", "Maintenance Extra"))
    TENANTS_CHOICES = (
        ("D", "Doesn't Matter"),
        ("F", "Family"),
        ("B", "Bachelor"),
        ("C", "Company"),
    )
    FURNISHING_CHOICES = (
        ("F", "Fully Furnishing"),
        ("S", "Semi Furnishing"),
        ("U", "Unfurnishing"),
    )
    PARKING_CHOICES = (("N", "None"), ("M", "Motorbike"), ("C", "Car"), ("B", "Both"))
    available_for = models.CharField(max_length=1, choices=AVAILABLE_FOR_CHOICES)
    expected_rent = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    expected_deposit = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=10
    )
    negotiable = models.BooleanField(default=False)
    maintenance = models.CharField(
        max_length=1, choices=MAINTENANCE_CHOICES, default="I", blank=True, null=True
    )
    available_from = models.DateField()
    tenants = models.CharField(max_length=1, choices=TENANTS_CHOICES, default="D")
    furnishing = models.CharField(max_length=1, choices=FURNISHING_CHOICES, default="F")
    parking = models.CharField(max_length=1, choices=PARKING_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.available_for

    class Meta:
        verbose_name_plural = "Rental Info"
        db_table = "property_rental"
        ordering = ["-created_on"]


class Gallery(CommonInfo):
    """
    Gallery
    """

    image = models.ImageField(upload_to="property/images")
    video = models.FileField(upload_to="property/videos")

    class Meta:
        verbose_name_plural = "Gallery"
        db_table = "propertys_gallery"

    def __str__(self):
        return str(self.id)


class Amenities(CommonInfo):
    """
    Amenities
    """

    YES_NO_CHOICES = (("Y", "Yes"), ("N", "No"))
    WATER_SUPPLY_CHOICES = (("C", "Corporation"), ("W", "Borewell"), ("B", "Both"))
    VIEWER_CHOICES = (
        ("H", "Need Help"),
        ("I", "I will show"),
        ("N", "Neighbours"),
        ("F", "Friends/Relatives"),
        ("S", "Security"),
        ("T", "Tenants"),
        ("O", "Others"),
    )
    bathrooms = models.IntegerField(default=0)
    balcony = models.CharField(max_length=63, choices=YES_NO_CHOICES, default="Y")
    water_supply = models.CharField(
        max_length=1, choices=WATER_SUPPLY_CHOICES, default="C"
    )
    gym = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    non_veg = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    security = models.CharField(max_length=1, choices=YES_NO_CHOICES, default="Y")
    viewer = models.CharField(max_length=1, choices=VIEWER_CHOICES, default="H")
    secondary_number = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Amenities"
        db_table = "property_amenities"

    def __str__(self):
        return str(self.bathrooms)


class PropertyInfo(CommonInfo):
    """
    Info about property
    """

    APARTMENT_CHOICES = (
        ("A", "Apartment"),
        ("I", "Independent House/Villa"),
        ("G", "Gated Community/Villa"),
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
    PROPERTY_TYPE_CHOICES = (
        ("R", "Residental"),
        ("C", "Commercial"),
    )
    PROPERTYAD_TYPE_CHOICES = (
        ("R", "Rent"),
        ("Re", "Resale"),
        ("P", "Pg/Hostel"),
        ("F", "Flatmates"),
        ("S", "Sale"),
    )
    property_type = models.CharField(
        max_length=1, choices=PROPERTY_TYPE_CHOICES, default="R"
    )
    property_adtype = models.CharField(
        max_length=2, choices=PROPERTYAD_TYPE_CHOICES, default="R"
    )
    apartment_type = models.CharField(
        max_length=1, choices=APARTMENT_CHOICES, default="A"
    )
    apartment_name = models.CharField(max_length=63, blank=True, null=True)
    bhk_type = models.CharField(
        max_length=20, choices=BHK_CHOICES, default="F"
    )  # bedroom hall kitchen
    floor = models.CharField(max_length=2, choices=NUMBER_OF_FLOOR_CHOICES, default="G")
    total_floor = models.CharField(
        max_length=2, choices=NUMBER_OF_FLOOR_CHOICES, default="G"
    )
    age = models.CharField(
        max_length=1, choices=AGE_CHOICES, default="U"
    )  # propertu age
    facing = models.CharField(max_length=2, choices=FACING_CHOICES)
    property_size = models.FloatField(default=0.00)
    city = models.CharField(max_length=60)
    locality = models.TextField()
    street = models.TextField()
    rental = models.ForeignKey(
        RentalInfo, on_delete=models.CASCADE, related_name="rental_info"
    )
    gallery = models.ManyToManyField(Gallery, related_name="gallery",)
    amenities = models.ForeignKey(
        Amenities, on_delete=models.CASCADE, related_name="amenities"
    )
    owner = models.ForeignKey(
        UserProfile,
        related_name="userprofile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    agent = models.ForeignKey(
        AgentDetail,
        related_name="agentdetail",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    staff = models.ForeignKey(
        StaffDetail,
        related_name="staffdetail",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # displaying the exact location using map
    location = models.PointField(null=True, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

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
        verbose_name_plural = "Property Info"
        db_table = "property"
        ordering = ["-created_on"]


class FieldVisit(CommonInfo):
    """"
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
    property_type = models.ForeignKey(
        PropertyInfo, related_name="discussion", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Property Discussion Board"
        db_table = "property_discussionboard"
