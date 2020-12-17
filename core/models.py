from django.db import models
from django.urls import reverse

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


PROPERTY_TYPE = (
    ("LA", "Land"),
    ("HO", "House"),
)

AD_TYPE = (
    ("RE", "Rential"),
    ("SA", "Sale"),
)

PROPERTY_FACING = (
    ("NO", "North"),
    ("EA", "East"),
    ("WE", "West"),
    ("SO", "SOuth"),
)

FURNISHING = (
    ("FU", "FUll"),
    ("SE", "Semi"),
)

# model for proerty detail


class PropertyDetail(models.Model):

    bhk = models.CharField(_("BHK"), max_length=50)
    floor_no = models.IntegerField(_("Floor Number"))
    total_floor = models.IntegerField(_("Total Floor"))
    property_age = models.IntegerField(_("Property Age"))
    facing = models.CharField(_("Property Facing"),
                              max_length=2, choices=PROPERTY_FACING)
    area = models.DecimalField(
        _("Property Area"), max_digits=10, decimal_places=2)
    size = models.CharField(_("Property Size"), max_length=100)

    class Meta:
        verbose_name = _("PropertyDetail")
        verbose_name_plural = _("PropertyDetails")

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("PropertyDetail_detail", kwargs={"pk": self.pk})


class LocalityDetail(models.Model):

    name = models.CharField(_("Loacality Name"), max_length=500)
    longitude = models.CharField(_("Longitude"), max_length=100)
    latitude = models.CharField(_("Latitude"), max_length=100)
    street = models.CharField(_("Street"), max_length=100)

    class Meta:
        verbose_name = _("LocalityDetail")
        verbose_name_plural = _("LocalityDetails")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("LocalityDetail_detail", kwargs={"pk": self.pk})


class Detail(models.Model):

    negotiable = models.BooleanField(_("Negotiable"), default=True)
    available_from = models.DateField(
        _("Available Date"), auto_now=False, auto_now_add=False)
    furnishing = models.CharField(_("Furnishing"), max_length=2)
    parking = models.CharField(_("Parking"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Detail")
        verbose_name_plural = _("Details")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Detail_detail", kwargs={"pk": self.pk})


class RentialDetail(Detail):

    expected_rent = models.DecimalField(
        _("Expected Rent"), max_digits=15, decimal_places=2)
    deposit = models.DecimalField(
        _("Expected Deposit"), max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = _("RentialDetail")
        verbose_name_plural = _("Rentia lDetails")

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("RentialDetail_detail", kwargs={"pk": self.pk})


class ResaleDetail(Detail):

    expected_price = models.DecimalField(
        _("Expected Price"), max_digits=25, decimal_places=2)
    construction_type = models.JSONField()

    class Meta:
        verbose_name = _("ResaleDetail")
        verbose_name_plural = _("ResaleDetails")

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("ResaleDetail_detail", kwargs={"pk": self.pk})


class Amenities(models.Model):

    bathorooms = models.IntegerField(_("Bathroom Count"))
    others = models.JSONField(_("Other INformations"))

    class Meta:
        verbose_name = _("Amenities")
        verbose_name_plural = _("Amenitiess")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Amenities_detail", kwargs={"pk": self.pk})


# Model for property


class Property(models.Model):

    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.SET_NULL)
    property_type = models.CharField(
        _("Property Type"), choices=PROPERTY_TYPE, max_length=2)
    ad_type = models.CharField(
        _("Property Ad Type"), max_length=50, choices=AD_TYPE)

    property_detail = models.OneToOneField(PropertyDetail, verbose_name=_(
        "Property Details"), on_delete=models.SET_NULL)
    locality_detail = models.OneToOneField(LocalityDetail, verbose_name=_(
        "Locality Details"), on_delete=models.SET_NULL)
    rential_detail = models.OneToOneField(RentialDetail, verbose_name=_(
        "Rential Details"), on_delete=models.SET_NULL)
    resale_detail = models.OneToOneField(ResaleDetail, verbose_name=_(
        "Resale Details"), on_delete=models.SET_NULL)
    amenities = models.OneToOneField(Amenities, verbose_name=_(
        "Amenities"), on_delete=models.SET_NULL)

    is_accepted = models.BooleanField(_("Accepted Property"), default=False)

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Propertys")

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("Property_detail", kwargs={"pk": self.pk})
