from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from .views import LoginUserView, RegisterUserView, ProfileUserView, CustomPasswordResetView, \
    CustomPasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

]