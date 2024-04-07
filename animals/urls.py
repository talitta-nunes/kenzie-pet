from django.urls import path

from . import views as animal_views

urlpatterns = [
    path("animals/", animal_views.AnimalView.as_view()),
    path("animals/<int:animal_id>/", animal_views.AnimalDetailView.as_view()),

]
