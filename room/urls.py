from django.urls import path
from .views import VideoView, VideoDetailView

urlpatterns = [
    path('video/', VideoView.as_view(), name='video'),
    path('video/<int:id>/', VideoDetailView.as_view(), name='video_detail'),
    ]
