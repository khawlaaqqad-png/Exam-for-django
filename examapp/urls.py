from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('shows', views.shows),
    path('logout', views.logout),
    path('show_creat', views.show_creat),
    path('create_show', views.create_show),
    path('delete_show/<int:show_id>', views.delete_show),
    path('edit_show/<int:show_id>', views.edit_show),
    path('show_details/<int:show_id>', views.show_details),
]