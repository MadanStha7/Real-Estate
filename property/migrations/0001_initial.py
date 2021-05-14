# Generated by Django 3.1 on 2021-05-13 08:42

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0003_auto_20210513_0725"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_auto_20210504_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_city_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "City",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="PropertyInfo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[("R", "Residential"), ("C", "Commercial")],
                        default="R",
                        max_length=1,
                    ),
                ),
                (
                    "property_adtype",
                    models.CharField(
                        choices=[
                            ("R", "Rent"),
                            ("Re", "Resale"),
                            ("P", "Pg/Hostel"),
                            ("F", "Flatmates"),
                            ("S", "Sale"),
                        ],
                        default="R",
                        max_length=2,
                    ),
                ),
                (
                    "apartment_type",
                    models.CharField(
                        choices=[
                            ("A", "Apartment"),
                            ("I", "Independent House/Villa"),
                            ("G", "Gated Community/Villa"),
                        ],
                        default="A",
                        max_length=1,
                    ),
                ),
                (
                    "apartment_name",
                    models.CharField(blank=True, max_length=63, null=True),
                ),
                (
                    "bhk_type",
                    models.CharField(
                        choices=[
                            ("1 RK", "1 RK"),
                            ("1 BHK", "1 BHK"),
                            ("2 BHK", "2 BHK"),
                            ("3 BHK", "3 BHK"),
                            ("4 BHK", "4 BHK"),
                            ("4+ BHK", "4+ BHK"),
                        ],
                        default="F",
                        max_length=20,
                    ),
                ),
                (
                    "floor",
                    models.CharField(
                        choices=[
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
                        ],
                        default="G",
                        max_length=2,
                    ),
                ),
                (
                    "total_floor",
                    models.CharField(
                        choices=[
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
                        ],
                        default="G",
                        max_length=2,
                    ),
                ),
                (
                    "age",
                    models.CharField(
                        choices=[
                            ("U", "Under Construction"),
                            ("L", "Less than a year"),
                            ("1", "1 to 3 year"),
                            ("3", "3 to 5 year"),
                            ("5", "5 to 10 year"),
                            ("M", "More than 10 year"),
                        ],
                        default="U",
                        max_length=1,
                    ),
                ),
                (
                    "facing",
                    models.CharField(
                        choices=[
                            ("E", "EAST"),
                            ("W", "WEST"),
                            ("N", "North"),
                            ("S", "South"),
                            ("NE", "North-East"),
                            ("SE", "South-East"),
                            ("NW", "North-West"),
                            ("SW", "South-West"),
                            ("D", "Don't Know"),
                        ],
                        max_length=2,
                    ),
                ),
                ("property_size", models.FloatField(default=0.0)),
                ("price", models.FloatField(default=0.0)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("publish", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
                ("views", models.PositiveIntegerField(default=0)),
                (
                    "listing_type",
                    models.CharField(
                        choices=[("T", "Top"), ("P", "Premium"), ("F", "Featured")],
                        max_length=1,
                    ),
                ),
                (
                    "membership_plan",
                    models.CharField(
                        choices=[("S", "Silver"), ("G", "Gold"), ("P", "Platinum")],
                        max_length=1,
                    ),
                ),
                (
                    "condition_type",
                    models.CharField(
                        choices=[("N", "New"), ("U", "Used")], max_length=1
                    ),
                ),
                (
                    "admin",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="admin_profile",
                        to="user.adminprofile",
                    ),
                ),
                (
                    "agent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agentdetail",
                        to="user.agentdetail",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="city_property",
                        to="property.city",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_propertyinfo_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userprofile",
                        to="user.userprofile",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staffdetail",
                        to="user.staffdetail",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Property Info",
                "db_table": "property",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "paint",
                    models.CharField(
                        blank=True,
                        choices=[("Y", "Yes"), ("N", "No")],
                        default="Y",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "cleaned",
                    models.CharField(
                        blank=True,
                        choices=[("Y", "Yes"), ("N", "No")],
                        default="Y",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "available_days",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("E", "Everyday(Sunday - Saturday)"),
                            ("W", "Weekdays(Sunday - Friday)"),
                            ("S", "Weekend(Saturday)"),
                        ],
                        default="E",
                        max_length=1,
                        null=True,
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "property_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="property_schedule",
                        to="property.propertyinfo",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Schedule",
                "db_table": "property_schedule",
            },
        ),
        migrations.CreateModel(
            name="RentalInfo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                (
                    "available_for",
                    models.CharField(
                        choices=[("R", "Only Rent"), ("L", "Only Lease")], max_length=1
                    ),
                ),
                (
                    "expected_rent",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "expected_deposit",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("negotiable", models.BooleanField(default=False)),
                (
                    "maintenance",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("I", "Maintenance Included"),
                            ("E", "Maintenance Extra"),
                        ],
                        default="I",
                        max_length=1,
                        null=True,
                    ),
                ),
                ("available_from", models.DateField()),
                (
                    "tenants",
                    models.CharField(
                        choices=[
                            ("D", "Doesn't Matter"),
                            ("F", "Family"),
                            ("B", "Bachelor"),
                            ("C", "Company"),
                        ],
                        default="D",
                        max_length=1,
                    ),
                ),
                (
                    "furnishing",
                    models.CharField(
                        choices=[
                            ("F", "Fully Furnishing"),
                            ("S", "Semi Furnishing"),
                            ("U", "Unfurnishing"),
                        ],
                        default="F",
                        max_length=1,
                    ),
                ),
                (
                    "parking",
                    models.CharField(
                        choices=[
                            ("N", "None"),
                            ("M", "Motorbike"),
                            ("C", "Car"),
                            ("B", "Both"),
                        ],
                        max_length=1,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_rentalinfo_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "property_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rental_info",
                        to="property.propertyinfo",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Rental Info",
                "db_table": "property_rental",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="PropertyRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=32, null=True)),
                ("phone", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                (
                    "request_type",
                    models.CharField(
                        choices=[("B", "Buy"), ("R", "Rent"), ("S", "Sell")],
                        max_length=1,
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("B", "House/Bungalow"),
                            ("F", "Flat & Apartment"),
                            ("C", "Commercial Property"),
                            ("L", "land"),
                            ("A", "Agricultural Land"),
                            ("O", "Office Space"),
                            ("S", "Shutter & Shop Space"),
                            ("R", "Restaurant for sale"),
                            ("H", "House in a Colony"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "urgent",
                    models.CharField(
                        choices=[
                            ("V", "Very Urgent"),
                            ("W", "Within a few days"),
                            ("M", "Within a month"),
                            ("I", "In few months time"),
                        ],
                        max_length=1,
                    ),
                ),
                ("place", models.TextField()),
                ("price_range", models.TextField()),
                (
                    "size",
                    models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
                ),
                ("description", models.TextField()),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_propertyrequest_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Property Request",
                "db_table": "property_request",
            },
        ),
        migrations.CreateModel(
            name="PropertyDiscussionBoard",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                (
                    "discussion",
                    models.CharField(
                        choices=[
                            ("Q", "Query"),
                            ("R", "Review"),
                            ("S", "Suggestion"),
                            ("C", "Complaint"),
                        ],
                        max_length=1,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        blank=True,
                        size=None,
                    ),
                ),
                ("comments", models.TextField()),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_propertydiscussionboard_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "property_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussion",
                        to="property.propertyinfo",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Property Discussion Board",
                "db_table": "property_discussionboard",
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("locality", models.TextField()),
                ("street", models.TextField()),
                (
                    "city",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="city_locations",
                        to="property.city",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_location_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "property_info",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to="property.propertyinfo",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Property Location",
                "db_table": "property_location",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Gallery",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("image", models.ImageField(upload_to="property/images")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_gallery_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "property_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery",
                        to="property.propertyinfo",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Gallery",
                "db_table": "propertys_gallery",
            },
        ),
        migrations.CreateModel(
            name="FieldVisit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("email", models.CharField(max_length=16)),
                ("phone", models.CharField(max_length=16)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_fieldvisit_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "property_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="field_visits",
                        to="property.propertyinfo",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Field Visit",
                "db_table": "property_field_visit",
                "ordering": ["-name"],
            },
        ),
        migrations.CreateModel(
            name="Amenities",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("bathrooms", models.IntegerField(default=0)),
                (
                    "balcony",
                    models.CharField(
                        choices=[("Y", "Yes"), ("N", "No")], default="Y", max_length=63
                    ),
                ),
                (
                    "water_supply",
                    models.CharField(
                        choices=[
                            ("C", "Corporation"),
                            ("W", "Borewell"),
                            ("B", "Both"),
                        ],
                        default="C",
                        max_length=1,
                    ),
                ),
                (
                    "gym",
                    models.CharField(
                        choices=[("Y", "Yes"), ("N", "No")], default="Y", max_length=1
                    ),
                ),
                (
                    "non_veg",
                    models.CharField(
                        choices=[("Y", "Yes"), ("N", "No")], default="Y", max_length=1
                    ),
                ),
                (
                    "security",
                    models.CharField(
                        choices=[("Y", "Yes"), ("N", "No")], default="Y", max_length=1
                    ),
                ),
                (
                    "viewer",
                    models.CharField(
                        choices=[
                            ("H", "Need Help"),
                            ("I", "I will show"),
                            ("N", "Neighbours"),
                            ("F", "Friends/Relatives"),
                            ("S", "Security"),
                            ("T", "Tenants"),
                            ("O", "Others"),
                        ],
                        default="H",
                        max_length=1,
                    ),
                ),
                ("secondary_number", models.IntegerField(default=1)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_amenities_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "property_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="amenities",
                        to="property.propertyinfo",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Amenities",
                "db_table": "property_amenities",
            },
        ),
    ]
