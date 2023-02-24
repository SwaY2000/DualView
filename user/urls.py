from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import InviteUserView, ActivateUserView, UserFriendView

urlpatterns = [
    path('user/', InviteUserView.as_view(), name='user'),
    path('user/activate/', ActivateUserView.as_view(), name='activate_user'),
    path('user/friend/', UserFriendView.as_view(), name='activate_user'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
