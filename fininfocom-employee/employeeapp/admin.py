from django.contrib import admin

# Register your models here.

from .models import Employee, AddressDetails, WorkExperience, Qualifications, Projects 

admin.site.register(Employee)
admin.site.register(AddressDetails)
admin.site.register(WorkExperience)
admin.site.register(Qualifications)
admin.site.register(Projects)
