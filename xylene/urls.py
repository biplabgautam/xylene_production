"""xylene URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import (login_view, change_credentials_view, logout_view, change_password_view)
from cms.views import subject_list

urlpatterns = [
    url(r'^$', subject_list, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^cms/', include("cms.urls", namespace='cms')),
    url(r'^tcms/', include("tempcms.urls", namespace = 'tcms')),
    url(r'^user/', include("accounts.urls", namespace = 'accounts')),
]

urlpatterns += url(r'^login/', login_view, name='login'),
urlpatterns += url(r'^logout/', logout_view, name='logout'),
urlpatterns += url(r'^change_credentials/', change_credentials_view, name='change_credentials'),
urlpatterns += url(r'^change_password/', change_password_view, name='change_password'),

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
