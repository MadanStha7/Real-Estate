from django.contrib import admin

from .models import (
    Property,
    Gallery,
    PropertyDiscussionBoard,
    FieldVisit,
    PropertyRequest,
)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ("uid", "owner", "agent", "bedrooms",)
    list_filter = ("owner", "agent", "bedrooms")
    # search_fields = ("storey",)


admin.site.register(Property, PropertyAdmin)
admin.site.register(Gallery)
admin.site.register(PropertyDiscussionBoard)
admin.site.register(FieldVisit)
admin.site.register(PropertyRequest)

