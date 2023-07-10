"""
URL configuration for sm_account app.
"""
from django.urls import path
import apps.sm_accounts.views as Account

urlpatterns = [
    path('signup/', Account.UserSignup.as_view(), name="user-signup"),
    path('login/', Account.UserLogin.as_view(), name="user-login"),
    path('logout/', Account.UserLogout.as_view(), name="user-logout"),
    # path('test_token/', Account.TestToken.as_view(), name="validate_token"),
    path('generate/otp/', Account.GenerateOTP.as_view(), name="generate-otp"),
    path('verify/otp/', Account.VerifyOTP.as_view(), name="verify-otp"),
]