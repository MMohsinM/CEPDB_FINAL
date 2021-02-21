from django.urls import path,include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('login/',views.userloginview),
    path('logout/',views.userlogoutview),
    #path('signup/',views.signup),
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate, name='activate'),
]