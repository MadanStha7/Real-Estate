from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ServiceProvider(models.Model):
    """
    model for service provider
    """
    user = models.ForeignKey(User, related_name='user_service', help_text="User listed service as provider")
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