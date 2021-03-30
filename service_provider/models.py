from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ServiceProvider(models.Model):
    """
    model for service provider
    """
    user = models.ForeignKey(User, related_name='user_service',
                             help_text="User listed service as provider",
                             on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.TextField()
    price = models.FloatField()
    contact_number = models.CharField(max_length=15)
    description = models.TextField()
    photos_or_videos = models.FileField(upload_to='user_service/')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name}"

    class Meta:
        db_table = 'service_provider'
        ordering = ['-added_at']


class BusinessHour(models.Model):
    """
    model for business hour
    """
    WEEKDAYS = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    STATUS = [
        ('O', 'OPEN'),
        ('C', 'CLOSE')
    ]
    service_provider = models.ForeignKey(ServiceProvider, related_name="service_business_hour",
                                         on_delete=models.CASCADE)
    day = models.IntegerField(choices=WEEKDAYS)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    status = models.CharField(max_length=6, choices=STATUS)

    def __str__(self):
        return f"{self.service_provider}"

    class Meta:
        db_table = "business_hours"
        ordering = ["day"]
