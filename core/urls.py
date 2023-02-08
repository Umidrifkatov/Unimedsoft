from django.urls import path
from .views import mainpage

urlpatterns = [
    path('', mainpage)
]
