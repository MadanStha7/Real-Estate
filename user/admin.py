from django.contrib import admin
from user.models import (
    AgentDetail,
    UserProfile,
    StaffDetail,
    Contact,
    AdminProfile,
    Notificatons,
    NotificationActivity,
)

# Register your models here.
admin.site.register(
    [
        AgentDetail,
        UserProfile,
        StaffDetail,
        AdminProfile,
        Contact,
        Notificatons,
        NotificationActivity,
    ]
)
