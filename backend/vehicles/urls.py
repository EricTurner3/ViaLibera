from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    UserViewSet,
    VehicleViewSet,
    FuelRecordViewSet,
    ServiceRecordViewSet,
    LoginView
)

router = DefaultRouter()
router.register(r'login', LoginView, basename='login')
router.register(r'users', UserViewSet, basename='user')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')

vehicles_router = NestedDefaultRouter(router, r'vehicles', lookup='vehicle')
vehicles_router.register(r'fuel-records', FuelRecordViewSet, basename='vehicle-fuel-record')
vehicles_router.register(r'service-records', ServiceRecordViewSet, basename='vehicle-service-record')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(vehicles_router.urls)),
] 