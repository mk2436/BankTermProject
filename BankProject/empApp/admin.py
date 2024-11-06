from django.contrib import admin
from empApp.models import Employee, Branch, Manager, AssistantMgr

admin.site.register(Employee)
admin.site.register(Branch)
admin.site.register(Manager)
admin.site.register(AssistantMgr)