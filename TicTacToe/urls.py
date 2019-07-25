"""TicTacToe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from .views import welcome

urlpatterns = [
    url('admin/', admin.site.urls),
    #path(r'welcome',welcome) # first arg is he urlname/pagename and second arg is the actual view function.
    # r is used for role string . A role string allows the use of special chars
    # the value of the role string is a regular expression which is use for pattern matching.for
    # So anything that starts with welcome will redirect you to the same welcome page Ex. Welcometoyou will
    # also call fucntion welcome.

    url(r'^$',welcome,name="tictactoe_welcome"),  # ^starts the string $ end of the string - for exact match
    url(r'^player/',include('player.urls')),
    url(r'^games/',include('playGame.urls'))
]
