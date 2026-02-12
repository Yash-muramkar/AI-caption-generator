from django.urls import path
from .views import upload, caption_history

urlpatterns = [
    path("", upload, name="upload"),
    path("history/", caption_history, name="caption_history"),
]
