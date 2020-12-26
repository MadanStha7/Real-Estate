from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

IDENTIFICATION_TYPE = (
    ('citizenship', 'Citizenship'),
    ('driving-license', 'Driving License'),
    ('others', 'Others')
)


class UserProfile(models.Model):
    """
    user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_picture = models.ImageField(upload_to='user/profile')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['-added_at']
        db_table = 'user_profile'


class AgentDetail(models.Model):
    """
    agent detail
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_detail')
    location = models.TextField()
    identification_type = models.CharField(choices=IDENTIFICATION_TYPE, max_length=20)
    identification_number = models.CharField(max_length=20)
    identification_file = models.FileField(upload_to='agent/identification')
    accept_terms_and_condition = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['-added_at']
        db_table = 'agent_detail'
