"""cit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
