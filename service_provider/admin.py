from django.contrib import admin

from service_provider.models import ServiceProvider, \
    Review, BusinessHours


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('service_name', "company_name", "location")
    list_filter = ('service_name', "company_name", "location")
    search_fields = ("service_name",)


admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Review)
admin.site.register(BusinessHours)
