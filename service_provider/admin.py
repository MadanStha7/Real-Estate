from django.contrib import admin

from service_provider.models import ServiceProvider, BusinessHour


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('service_name', "company_name", "location")
    list_filter = ('service_name', "company_name", "location")
    search_fields = ("service_name",)


admin.site.register(ServiceProvider, ServiceProviderAdmin)


class BusinessHourAdmin(admin.ModelAdmin):
    list_display = ("service_provider", 'day', "status")
    list_filter = ("service_provider", 'day', "status")
    search_fields = ("service_provider",)


admin.site.register(BusinessHour, BusinessHourAdmin)
