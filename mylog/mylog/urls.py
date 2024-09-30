
from django.contrib import admin
from django.urls import path, include
from myapp import views




urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.register, name='register'),
    path("user_login/", views.user_login, name="login"),
    path("user_logout/", views.user_logout, name='logout'),
    path("home/", views.home, name='home'),
    path("delete/<int:person_id>/", views.delete_person, name='delete_person'),


]
