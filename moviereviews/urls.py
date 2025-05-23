"""
URL configuration for moviereviews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from movie import views as movieViews
from news import views as newsViews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", movieViews.home, name="home"),
    path('admin/', admin.site.urls),
    path("about/", movieViews.about, name="about"),
    path("news/", newsViews.news, name="news"),
    path("statistics/", movieViews.statistics_views, name="statistics"),
    path("signup/", movieViews.signup, name="signup"),
    #path("login/", movieViews.login, name="login"),
    path("iarecommendation/", movieViews.iarecommendation, name="iarecommendation"),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
