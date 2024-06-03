from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import *


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/', googleSignInAcc, name='google'),
    path('test/', new, name='NewTest'),
    path('healthData/', healthData, name='health-data'),
    path("challenge", ChallengeView.as_view(), name='challenge'),
    path("getUserDetails", getUserDetails, name='getUserDetails'),
    path("getFriends", getFriends, name='getFriends'),
    path("getPrivacyPolicy", getPrivacyPolicy, name='getPrivacyPolicy'),
]