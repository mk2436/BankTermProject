from django.contrib import admin
from django.urls import path
from rootApp.views import home, user_profile
from empApp.views import emp_login, mgr_login, user_logout, create_customer, delete_customer, create_employee

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('user-profile/', user_profile, name='user-profile'),
    path('emp-login/',emp_login,name='emp-login'),
    path('mgr-login/',mgr_login,name='mgr-login'),
    path('user-logout/',user_logout, name='user-logout'),
    path('emp/create-customer/', create_customer, name = 'create-customer'),
    path('mgr/create-emp/', create_employee, name='create-emp' ),
    path('emp/del-customer/',delete_customer, name = 'del-customer')
]
