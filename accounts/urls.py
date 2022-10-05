from django.urls import path
from .views import login, register, logout, VerificationView, password_reset_request
# from django.contrib.auth import views as auth_views
app_name = "accounts"

urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout, name="logout"),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name="activate"),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('password_reset/', password_reset_request, name="password_reset"),
    
]