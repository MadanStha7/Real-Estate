from django.contrib import admin

from property.models import (
    Property, SocietyAmenities,
    PropertyGallery, PropertyDiscussionBoard, FieldVisit)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ("uid", 'owner', "agent", "bedrooms", "storey")
    list_filter = ("owner", "agent", "bedrooms", "storey")
    search_fields = ("storey",)


admin.site.register(Property, PropertyAdmin)
admin.site.register(SocietyAmenities)
admin.site.register(PropertyGallery)
admin.site.register(PropertyDiscussionBoard)
admin.site.register(FieldVisit)

