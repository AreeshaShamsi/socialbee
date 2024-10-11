
from django.urls import path
from . import views	
from uuid import UUID

urlpatterns=[
    path('',views.index,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('search',views.search,name='search'),
    path('logout',views.user_logout,name='logout'),
    path('settings',views.settings,name='settings'),
    path('upload',views.upload,name='upload'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('follow',views.follow,name='follow'),
    
    

]
