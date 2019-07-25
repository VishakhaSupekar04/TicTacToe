from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from .views import home, new_invite, accept_invite, SignUpView


urlpatterns = [
    url(r'home$',home, name="player_home"),
    url(r'login$',
        LoginView.as_view(template_name="player/login.html"),
        name="player_login"),
    url(r'logout$',
        LogoutView.as_view(),
        name="player_logout"),
    url(r'new_invite$',
        new_invite,
        name="player_new_invite"),
    url(r'accept_invite/(?P<id>\d+)/$',
        accept_invite,
        name="player_accept_invite"),
    url(r'signup$', SignUpView.as_view(), name='player_signup'),
]