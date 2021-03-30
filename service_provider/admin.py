from django.contrib import admin

<<<<<<< HEAD
from service_provider.models import ServiceProvider, BusinessHour
=======
from service_provider.models import ServiceProvider, \
    Review, BusinessHours
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('service_name', "company_name", "location")
    list_filter = ('service_name', "company_name", "location")
    search_fields = ("service_name",)


admin.site.register(ServiceProvider, ServiceProviderAdmin)
<<<<<<< HEAD


class BusinessHourAdmin(admin.ModelAdmin):
    list_display = ("service_provider", 'day', "status")
    list_filter = ("service_provider", 'day', "status")
    search_fields = ("service_provider",)


admin.site.register(BusinessHour, BusinessHourAdmin)
=======
admin.site.register(Review)
admin.site.register(BusinessHours)
>>>>>>> ca6542c0c2b43777234cb2a08d3b5bbff8644362
