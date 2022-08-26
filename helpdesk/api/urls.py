from .views import save_hardware_to_db
from django.urls import path

urlpatterns = [
    path('getData/', save_hardware_to_db, name="getData")
]

