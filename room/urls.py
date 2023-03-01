from django.urls import path
from .views import VideoView, VideoDetailView, VideoListView

urlpatterns = [
    path('video/', VideoView.as_view(), name='video'),
    path('video/all/', VideoListView.as_view(), name='video_list'),
    path('video/<int:id>/', VideoDetailView.as_view(), name='video_detail'),
]
