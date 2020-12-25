from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class SocietyAmenities(models.Model):
    title = models.CharField(max_length=32)
    style_class = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = "property_society_amenities"


class Property(models.Model):
    MEMBERSHIP_PLAN_CHOICES = (
        ('S', 'Silver'),
        ('G', 'Gold'),
        ('P', 'Platinum'),
    )
    CONDITION_CHOICES = (
        ('N', 'New'),
        ('U', 'Used'),
    )
    PROPERTY_TYPE_CHOICES = (
        ('H', 'House'),
        ('L', 'Land'),
        ('F', 'Flat'),
    )
    FACING_CHOICES = (
        ('E', 'EAST'),
        ('W', 'WEST'),
        ('N', 'North'),
        ('S', 'South'),
    )
    DEVELOPMENT_PROGRESS_STATUS = (
        ('N', 'Initial State'),
        ('I', 'In Progress'),
        ('R', 'Ready'),
    )
    AVAILABLE_FOR_CHOICES = (
        ('R', 'Rent'),
        ('s', 'Sale'),
    )
    owner = models.ForeignKey(User, related_name="properties", on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name="agent_properties", on_delete=models.CASCADE)
    membership_plan = models.CharField(max_length=1, choices=MEMBERSHIP_PLAN_CHOICES)
    development_progress_status = models.CharField(max_length=1, choices=DEVELOPMENT_PROGRESS_STATUS)
    bedroom_hall_kitchen = models.IntegerField(default=0)
    land_area = models.FloatField(default=0.00)
    build_up_area = models.FloatField(default=0.00)
    address = models.TextField()
    uid = models.UUIDField(unique=True, auto_created=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    condition_type = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    available_from = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=63, blank=True, null=True)
    available_for = models.CharField(max_length=1, choices=AVAILABLE_FOR_CHOICES)
    storey = models.IntegerField(default=1)
    parking = models.IntegerField(default=0)
    attached_bathroom = models.IntegerField(default=0)
    facing = models.CharField(max_length=1, choices=FACING_CHOICES)
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPE_CHOICES)
    furnished = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    viewed_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    society_amenities = models.ManyToManyField(SocietyAmenities)
    location = models.PointField(null=True, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.property_type
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.location:
            self.latitude = self.location.x
            self.longitude = self.location.y
        elif self.longitude and self.latitude:
            self.location = Point(self.longitude, self.latitude, srid=4326)
        super(Property, self).save(force_insert=False,
                                   force_update=False, using=None, update_fields=None)

    class Meta:
        db_table = "property_property"
        get_latest_by = ['-membership_plan', '-added_at']
        ordering = ['-membership_plan', '-added_at']
        permissions = [('has_agent_permission', 'Can Show Property')]

        indexes = [
            models.Index(fields=['city', 'condition_type']),
            models.Index(fields=['city', 'available_for', 'condition_type']),
            models.Index(fields=['available_for', 'condition_type']),
            models.Index(fields=['city', 'available_for']),
            models.Index(fields=['storey'], name='storey_idx'),
            models.Index(fields=['parking'], name='parking_idx'),
            models.Index(fields=['facing'], name='facing_idx'),
        ]


class PropertyGallery(models.Model):
    image = models.ImageField(upload_to="property/images")
    property = models.ForeignKey(Property, related_name="gallery", on_delete=models.CASCADE)

    class Meta:
        db_table = "property_property_gallery"
