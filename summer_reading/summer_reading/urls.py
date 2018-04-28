"""summer_reading URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .views import (UserRegisterView, UserAccountView, CreateReview, ReviewView, HomeView)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home-page'),
    url(r'^admin/', admin.site.urls),
    url(r'^users/login/$', auth_views.LoginView.as_view() , name='auth_login'),
    url(r'^users/logout/$', auth_views.LogoutView.as_view(), name='auth_logout'),
    url(r'^users/signup/$', UserRegisterView.as_view(), name='user-registration'),
    url(r'^users/account/$', UserAccountView.as_view(), name='user-account'),
    url(r'^add_review', CreateReview.as_view(), name='add-review'),
    url(r'^users/review/(?P<review_id>\d+)/$', ReviewView.as_view(), name='review'),
]
