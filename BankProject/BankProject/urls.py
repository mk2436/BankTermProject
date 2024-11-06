from django.contrib import admin
from django.urls import path
from rootApp.views import home
from empApp.views import emp_login, mgr_login, emp_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('emp-login/',emp_login,name='emp-login'),
    path('mgr-login/',mgr_login,name='mgr-login'),
    path('emp-logout/',emp_logout, name='emp-logout'),
]
