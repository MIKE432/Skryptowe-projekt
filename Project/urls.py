"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views
from webapp.views import user, training

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'api/users/', user.UserList.as_view()),
    path(r'api/users/<int:user_id>/', user.UserDetails.as_view()),
    path(r'api/users/login/', user.UserLogin.as_view()),
    path(r'api/users/register/', user.UserRegister.as_view()),

    path(r'api/trainings/<int:training_id>/', training.Training.as_view())
]