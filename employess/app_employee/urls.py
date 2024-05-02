from django.urls import path
from .views import main_view
from .consumer import Consumer
urlpatterns = [
    path('', main_view, name='main'),
]
