from django.urls import path
from api.v1.task import views

urlpatterns=[
    path('admin_stats',views.admin_stats)
]