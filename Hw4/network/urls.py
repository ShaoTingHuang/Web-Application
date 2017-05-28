from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from network import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add-item$', views.add_item, name='add'),
    url(r'^delete-item/(?P<item_id>\d+)/(?P<user_name>.*)$', views.delete_item, name='delete'),
    url(r'^login$', auth_views.login, {'template_name':'network/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile/(?P<user_name>.*)$', views.profile, name='profile'),
    url(r'^home$', views.home, name='home'),
    url(r'^photo/(?P<user_name>.*)', views.get_photo, name='photo'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^follow/(?P<user_name>.*)',views.follow, name = 'follow'),
    url(r'^unfollow/(?P<user_name>.*)',views.unfollow,name='unfollow'),
    url(r'^followstream$',views.followstream,name='followstream')
]
