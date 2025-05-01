"""
URL configuration for backend project.

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
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Add 'api/' prefix here
    path('api/boxes/', views.BoxList.as_view(), name='box-list'),  # Add BoxList view
    path('api/boxes/<int:pk>/', views.BoxDetail.as_view(), name='box-detail'),  # Add BoxDetail view
    path('api/packed-boxes/', views.PackedBoxList.as_view(), name='packed-box-list'),  # PackedBoxList view
    path('api/packed-boxes/<int:pk>/', views.PackedBoxDetail.as_view(), name='packed-box-detail'),  # PackedBoxDetail view
]
