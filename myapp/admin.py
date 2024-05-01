from django.contrib import admin

from .models import Attendance, UserProfile

# To change the header of admin dashboard
admin.site.site_header = "Attendence MGMT Dashboard"

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Attendance)