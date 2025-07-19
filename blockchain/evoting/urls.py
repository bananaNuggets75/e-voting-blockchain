from django.urls import path
from . import views

urlpatterns = [
    path('vote/', views.vote, name='vote'),
]
