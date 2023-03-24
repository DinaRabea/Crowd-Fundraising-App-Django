from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup', views.AddUser, name='signup'),
    path('activate/<uuid:token>/', views.activate, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.user_login, name='login'),
    path('api', views.all_users, name='api_all'),
    path('api/<int:id>', views.one_user, name='api_one'),
]
