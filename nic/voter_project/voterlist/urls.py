from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voter_list'),
    path('pdf/', views.generate_pdf, name='generate_pdf'),
]