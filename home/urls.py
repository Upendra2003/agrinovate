from django.urls import path
from . import views 
from .views import SoilHealthCreateView

urlpatterns = [
    path('', views.info_view, name='info_view'), 
      path('api/soil-health/', SoilHealthCreateView.as_view(), name='soil-health-create'),
    
]

