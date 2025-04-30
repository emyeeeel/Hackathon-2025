from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.FreightDataViewSet.as_view(), name='freight-data'),
]