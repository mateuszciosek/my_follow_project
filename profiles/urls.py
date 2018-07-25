from django.contrib import admin
from django.urls import path, include


from . import views

urlpatterns = [
    path('details/', views.UserProfile.as_view(), name="user_profile"),
    path('edit/', views.edit_account, name="user_account_edit"),
    path('add_follow/<int:pk>/', views.add_follow, name='add_follow'),
    path('unfollow/<int:pk>/', views.unfollow, name="unfollow"),
    path('cancel_request/<int:pk>/', views.cancel_request, name="cancel_request"),
    path('request_follow/', views.RequestListView.as_view(),
         name="request_follow_list"),
    path('accept_follow/<int:pk>', views.accept_follow, name="accept_follow"),
    path('<slug>/', views.ProfileDetails.as_view(), name="profile_details"),
]
