from django.db import models
from django.contrib.auth import get_user_model
from common.models import CommonInfo
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

User = get_user_model()

IDENTIFICATION_TYPE = (
    ("citizenship", "Citizenship"),
    ("driving-license", "Driving License"),
    ("others", "Others"),
)
class AgentDetail(CommonInfo):
    """
    agent detail
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="agent_detail"
    )
    location = models.TextField()
    identification_type = models.CharField(choices=IDENTIFICATION_TYPE, max_length=20)
    identification_number = models.CharField(max_length=20)
    identification_file = models.FileField(
        upload_to="agent/identification", blank=True, null=True
    )
    accept_terms_and_condition = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Agent")
        print("group",group)
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ["-added_at"]
        db_table = "agent_detail"


class UserProfile(CommonInfo):
    """
    Buyer and seller profile
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="buyer_seller_profile"
    )

    full_name = models.CharField(max_length=60, blank=True)
    profile_picture = models.ImageField(
        upload_to="user/buyerseller", blank=True, null=True
    )
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="BuyerOrSeller")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ["-added_at"]
        db_table = "Buyer/Seller"


class StaffDetail(CommonInfo):
    """
    Employee staff detail
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_detail"
    )
    full_name = models.CharField(max_length=60, blank=True)
    profile_picture = models.ImageField(upload_to="user/staff", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Staff")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ["-id"]
        db_table = "staff_detail"



class Contact(models.Model):
    """
    Contact us page
    """
    name = models.CharField(max_length=60, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Contact us"

    def __name__(self):
        return self.email