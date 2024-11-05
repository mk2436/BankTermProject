from django.contrib import admin

# Register your models here.
from .models import Employee, Branch

admin.site.register(Employee)
admin.site.register(Branch)