from django.urls import path
from .views import map_view, ready_map,ready_map_hour

urlpatterns = [
    path('', map_view, name='map_view'),
    path('ready', ready_map, name='ready_map'),
    path('ready_hour', ready_map_hour, name='ready_map'),
]