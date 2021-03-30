<<<<<<< HEAD
# Generated by Django 3.1 on 2021-03-22 09:02
=======
# Generated by Django 3.1 on 2021-03-26 07:03
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('image', models.ImageField(upload_to='property/images')),
                ('video', models.FileField(upload_to='property/videos')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_gallery_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'db_table': 'property_gallery',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(auto_created=True, blank=True, null=True, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('commercial', models.CharField(blank=True, choices=[('R', 'Rent'), ('S', 'Sale')], max_length=1, null=True)),
<<<<<<< HEAD
                ('residential', models.CharField(blank=True, choices=[('R', 'Rent'), ('R', 'Resale'), ('P', 'Pg/Hostel'), ('F', 'Flatmates')], max_length=1, null=True)),
=======
                ('residential', models.CharField(blank=True, choices=[('R', 'Rent'), ('S', 'Resale'), ('P', 'Pg/Hostel'), ('F', 'Flatmates')], max_length=1, null=True)),
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
                ('apartment', models.CharField(choices=[('A', 'Apartment'), ('I', 'Independent House/Villa'), ('G', 'Gated Community/Villa')], default='A', max_length=1)),
                ('apartment_name', models.CharField(blank=True, max_length=63, null=True)),
                ('floor', models.CharField(choices=[('G', 'Ground'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')], default='G', max_length=2)),
                ('storey', models.CharField(choices=[('G', 'Ground'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')], default='G', max_length=2)),
                ('age', models.CharField(choices=[('U', 'Under Construction'), ('L', 'Less than a year'), ('1', '1 to 3 year'), ('3', '3 to 5 year'), ('5', '5 to 10 year'), ('M', 'More than 10 year')], default='U', max_length=1)),
                ('listing_type', models.CharField(choices=[('T', 'Top'), ('P', 'Premium'), ('F', 'Featured')], default='T', max_length=1)),
                ('membership_plan', models.CharField(choices=[('S', 'Silver'), ('G', 'Gold'), ('P', 'Platinum')], default='S', max_length=1)),
                ('development_progress_status', models.CharField(choices=[('N', 'Initial State'), ('I', 'In Progress'), ('R', 'Ready')], default='N', max_length=1)),
                ('bedroom_hall_kitchen', models.IntegerField(default=0)),
                ('land_area', models.FloatField(default=0.0)),
                ('build_up_area', models.FloatField(default=0.0)),
                ('city', models.CharField(blank=True, max_length=63, null=True)),
                ('address', models.TextField()),
<<<<<<< HEAD
                ('locality', models.CharField(default='A', max_length=63)),
=======
                ('locality', models.CharField(max_length=63)),
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('condition_type', models.CharField(choices=[('N', 'New'), ('U', 'Used')], max_length=1)),
                ('available_for', models.CharField(choices=[('R', 'Only Rent'), ('L', 'Only Lease')], max_length=1)),
                ('expected_rent', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('expected_deposit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('negotiable', models.BooleanField(default=False)),
                ('maintenance', models.CharField(choices=[('I', 'Maintenance Included'), ('E', 'Maintenance Extra')], default='I', max_length=1)),
<<<<<<< HEAD
                ('available_from', models.DateField(blank=True, null=True)),
=======
                ('available_from', models.DateField()),
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
                ('tenants', models.CharField(choices=[('D', "Doesn't Matter"), ('F', 'Family'), ('B', 'Bachelor'), ('C', 'Company')], default='D', max_length=1)),
                ('furnishing', models.CharField(choices=[('F', 'Fully Furnishing'), ('S', 'Semi Furnishing'), ('U', 'Unfurnishing')], default='F', max_length=1)),
                ('parking', models.CharField(choices=[('N', 'None'), ('M', 'Motorbike'), ('C', 'Car'), ('B', 'Both')], max_length=1)),
                ('description', models.TextField()),
                ('bedrooms', models.IntegerField(default=0)),
                ('bathrooms', models.IntegerField(default=0)),
                ('balcony', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=63)),
                ('water_supply', models.CharField(choices=[('C', 'Corporation'), ('W', 'Borewell'), ('B', 'Both')], default='C', max_length=1)),
                ('gym', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1)),
                ('non_veg', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1)),
                ('security', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1)),
                ('viewer', models.CharField(choices=[('H', 'Need Help'), ('I', 'I will show'), ('N', 'Neighbours'), ('F', 'Friends/Relatives'), ('S', 'Security'), ('T', 'Tenants'), ('O', 'Others')], default='H', max_length=1)),
                ('secondary_number', models.IntegerField(default=1)),
                ('attached_bathroom', models.IntegerField(default=0)),
                ('facing', models.CharField(choices=[('E', 'EAST'), ('W', 'WEST'), ('N', 'North'), ('S', 'South'), ('NE', 'North-East'), ('SE', 'South-East'), ('NW', 'North-West'), ('SW', 'South-West'), ('D', "Don't Know")], max_length=2)),
                ('paint', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1)),
                ('cleaned', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1)),
                ('available_days', models.CharField(choices=[('E', 'Everyday(Sunday - Saturday)'), ('W', 'Weekdays(Sunday - Friday)'), ('S', 'Weekend(Saturday)')], default='E', max_length=1)),
<<<<<<< HEAD
                ('start_time', models.TimeField(auto_now=True)),
                ('end_time', models.TimeField(auto_now=True)),
=======
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
                ('property_type', models.CharField(choices=[('H', 'House'), ('L', 'Land'), ('F', 'Flat')], max_length=1)),
                ('furnished', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('viewed_count', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_properties', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_property_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('gallery', models.ManyToManyField(related_name='property_gallerys', to='property.Gallery')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'property_property',
                'ordering': ['-membership_plan', '-added_at'],
                'permissions': [('has_agent_permission', 'Can Show Property')],
                'get_latest_by': ['-membership_plan', '-added_at'],
            },
        ),
        migrations.CreateModel(
            name='SocietyAmenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('title', models.CharField(max_length=32)),
                ('style_class', models.CharField(blank=True, max_length=32, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_societyamenities_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'db_table': 'property_society_amenities',
            },
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='PropertyDiscussionBoard',
=======
            name='PropertyRequest',
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
<<<<<<< HEAD
                ('discussion', models.CharField(choices=[('Q', 'Query'), ('R', 'Review'), ('S', 'Suggestion'), ('C', 'Complaint')], max_length=1)),
                ('title', models.CharField(blank=True, max_length=32, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), blank=True, size=None)),
                ('comments', models.TextField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_propertydiscussionboard_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussion', to='property.property')),
            ],
            options={
=======
                ('name', models.CharField(max_length=63)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('request_type', models.CharField(choices=[('B', 'Buy'), ('R', 'Rent'), ('S', 'Sell')], max_length=1)),
                ('property_type', models.CharField(choices=[('B', 'House/Bungalow'), ('F', 'Flat & Apartment'), ('C', 'Commercial Property'), ('L', 'Land'), ('A', 'Agricultural Land'), ('O', 'Office Space'), ('S', 'Shutter & Shop Space'), ('R', 'Restaurant for Sale'), ('H', 'House in a Colony')], max_length=1)),
                ('urgent', models.CharField(choices=[('V', 'Very Urgent'), ('D', 'Within a few days'), ('M', 'Within a month'), ('F', 'in few months time')], max_length=1)),
                ('property_address', models.CharField(max_length=63)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('parking_space', models.FloatField()),
                ('bedrooms', models.IntegerField(default=0)),
                ('size', models.FloatField()),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_propertyrequest_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'db_table': 'property_request',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PropertyDiscussionBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('discussion', models.CharField(choices=[('Q', 'Query'), ('R', 'Review'), ('S', 'Suggestion'), ('C', 'Complaint')], max_length=1)),
                ('title', models.CharField(blank=True, max_length=32, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), blank=True, size=None)),
                ('comments', models.TextField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_propertydiscussionboard_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussion', to='property.property')),
            ],
            options={
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
                'db_table': 'property_property_discussion',
            },
        ),
        migrations.AddField(
            model_name='property',
            name='society_amenities',
            field=models.ManyToManyField(related_name='amenities', to='property.SocietyAmenities'),
        ),
        migrations.CreateModel(
            name='FieldVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=16)),
                ('phone', models.CharField(max_length=16)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_fieldvisit_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_visits', to='property.property')),
            ],
            options={
                'db_table': 'property_field_visit',
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city', 'condition_type'], name='property_pr_city_5e8ab3_idx'),
<<<<<<< HEAD
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city', 'commercial', 'condition_type'], name='property_pr_city_fa0210_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city', 'residential', 'condition_type'], name='property_pr_city_8cba20_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['storey'], name='storey_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['parking'], name='parking_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
=======
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city', 'commercial', 'condition_type'], name='property_pr_city_fa0210_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city', 'residential', 'condition_type'], name='property_pr_city_8cba20_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['storey'], name='storey_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['parking'], name='parking_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
            index=models.Index(fields=['facing'], name='facing_idx'),
        ),
    ]
