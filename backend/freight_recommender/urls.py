from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'freight', views.FreightTypeViewSet)
router.register(r'container-types', views.ContainerTypeViewSet)
router.register(r'load-types', views.LoadTypeViewSet)
router.register(r'cargo-categories', views.CargoCategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('data/', views.FreightDataView.as_view(), name='freight-data'),
    path('recommendation/', views.FreightRecommendationView.as_view(), name='freight-recommend'),
]