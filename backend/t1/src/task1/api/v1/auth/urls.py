from django.urls import path
from api.v1.auth import views

urlpatterns = [
    path('signup', views.signup),
    path('login',views.login),

    path('users',views.users),
    path('users/<int:id>',views.userdetails),

    path('admin_user',views.admin_user)
]