from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload, name="upload"),
    path("history/", views.caption_history, name="caption_history"),
    path("generate-caption/", views.generate_caption, name="generate_caption"),
]
