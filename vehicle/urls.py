from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='vehicle-index'),
    path('detail/<int:primary_key>', views.vehicle_detail_view, name='vehicle-detail')
]
