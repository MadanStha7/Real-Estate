import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from common.models import CommonInfo


User = get_user_model()


class BusinessHours(CommonInfo):
    day = models.CharField(max_length=15)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        db_table = "business_hours"

    def __str__(self):
        return self.day


class ServiceProvider(CommonInfo):
    """
    model for service provider
    """
    user = models.ForeignKey(User, related_name='user_service',
                             help_text="User listed service as provider",
                             on_delete=models.CASCADE)
    uid = models.UUIDField(unique=True, auto_created=True, null=True, blank=True)
    service_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    address = models.TextField(blank=True,)
    price = models.FloatField()
    contact_number = models.CharField(max_length=15)
    description = models.TextField()
    photos_or_videos = models.FileField(upload_to='user_service/')
    added_at = models.DateTimeField(auto_now_add=True)
    location = models.PointField(null=True, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    business_hour = models.ManyToManyField(
        BusinessHours, related_name="business_hours",
    )

    def __str__(self):
        return f"{self.service_name}"

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        if self.location:
            self.latitude = self.location.y
            self.longitude = self.location.x

        elif self.latitude and self.longitude:
            self.location = Point(x=self.longitude, y=self.latitude, srid=4326)

        super(ServiceProvider, self).save(*args, **kwargs)

    class Meta:
        db_table = 'service_provider'
        ordering = ['-added_at']


class Review(CommonInfo):
    RECOMMEND_CHOICES = (
        ("Y", "YES"),
        ("N", "NO"),
    )
    RATING_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )
    user = models.ForeignKey(User, related_name='review_user',
                             help_text="User listed service as provider",
                             on_delete=models.CASCADE)
    service_provider = models.ForeignKey(
        ServiceProvider, related_name="review", on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    description = models.TextField()
    recommend = models.CharField(max_length=1, choices=RECOMMEND_CHOICES)

    def __str__(self):
        return self.user

    class Meta:
        db_table = "service_review"
        ordering = ['-rating']



