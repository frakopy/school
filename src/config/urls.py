from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Root URL
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    # grappelli URLS
    path('grappelli/', include('grappelli.urls')),
    #Admin URL
    path('admin/', admin.site.urls),
    # Paths for records
    path('attendance/', include('records.urls')),
    # Paths for teachers
    path('home_teachers/', include('teachers.urls')),
    # Paths for Goals
    path('goal/', include('goals.urls')),
    # Paths for Authentication
    path('authentication/', include('authentication.urls')),
]
