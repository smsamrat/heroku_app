from django.contrib import admin
from django.urls import path
from App_account import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('custom-profile/', views.custom_profile, name='custom_profile'),
    path('custom-change-profile/', views.change_profile, name='change_profile'),
    path('add-profile-pic/', views.add_profile_pic, name='add_profile_picture'),
    path('edit-profile-pic/', views.edit_profile_picture, name='edit_profile_picture'),
]