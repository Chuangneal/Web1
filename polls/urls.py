
from django.urls import path

from . import views

app_name = 'polls'  # To active <appname>:<suburl>
urlpatterns = [

    # Index
    path('', views.home, name='index'),

    # Upload
    path('upload_action/', views.upload_action, name='upload_action'),

    # Home
    path('home/', views.home, name='home'),
    # Vote
    path('<str:poster_name>/vote/', views.vote, name='vote'),
    # Detail
    path('<str:poster_name>/detail/', views.detail, name='detail'),
    # Download
    path('<str:poster_name>/download/', views.download, name='download'),
    # Popular
    path('popular/', views.popular, name='popular'),
    # Best
    path('best/', views.best, name='best'),

    # Staff pages
    path('coordinator/', views.coordinator, name='coordinator'),
    path('programme_judge/', views.programme_judge, name='programme_judge'),
    path('head_judge/', views.head_judge, name='head_judge'),
    path('myadmin/', views.admin, name='myadmin'),
    path('chairman/', views.chairman, name='chairman'),

    # Login
    path('<str:login_type>/login/', views.login, name='login'),
    # Logout
    path('logout/', views.logout, name='logout'),

    

]
