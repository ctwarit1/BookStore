from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserReg.as_view(), name='user'),
    path('login/', views.UserLog.as_view(), name='login'),
    path('verify_user/', views.VerifyUser.as_view(), name='verify_user')
]
