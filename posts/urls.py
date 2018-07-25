from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.FollowersPostListView.as_view(), name="dashboard"),
    path('your_posts/', views.UserPostListView.as_view(), name="user_posts"),
    path('new/', views.CreatePostView.as_view(), name="post_new"),
    path('<int:pk>/edit/', views.PostEdit.as_view(), name="post_edit"),
    path('<int:pk>/delete/', views.PostRemove.as_view(), name="post_remove"),
    path('<int:pk>/', views.PostDetail.as_view(), name="post_detail"),
    path('<int:pk>/comment/', views.add_comment_to_post,
         name="add_comment_to_post"),
    path('<int:pk>/post_list/', views.AnotherUserPostListView.as_view(),
         name="user_post_list"),
]
