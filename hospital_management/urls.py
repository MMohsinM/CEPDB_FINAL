"""hospital_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import login
from django.urls import path,include
from accounts.views import home_page
from hospital.views import disease_list_admin, admin_action_disease, admin_create_hospital
from django.conf import settings
from django.conf.urls.static import static

#
import debug_toolbar
#

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_page),
    path('accounts/',include('accounts.urls')),
    path('hospital/',include('hospital.urls')),
    path('admin-disease-list/',disease_list_admin),
    path('disease-action-admin/<str:action>/<int:dd_id>/',admin_action_disease),
    path('admin-create-hospital/',admin_create_hospital),
    #
    path('__debug__/', include(debug_toolbar.urls)),
    #
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
