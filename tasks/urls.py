from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('menadevs-admins1130/', admin.site.urls),
    path('', views.submit_task, name='submit_task'),
    path('success/', views.success, name='success'),
    ]