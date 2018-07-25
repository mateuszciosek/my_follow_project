from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from profiles import views as prof_views
from posts import views as post_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', prof_views.Register.as_view(), name='index'),
    path('login/', views.login, {'template_name': "index.html"}, name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/', include('profiles.urls')),
    path('user_list/', prof_views.UserList.as_view(), name='user_list'),
    path('success/', prof_views.SuccessRegister.as_view(), name="success"),
    path('main/', include('posts.urls')),
    path('post/', include('posts.urls')),
]
