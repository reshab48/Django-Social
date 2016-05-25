from django.conf.urls import include, url
from .views import register, edit, dashboard, user_list, user_detail, user_follow, add_location

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^logout_then_login$', 'django.contrib.auth.views.logout_then_login', name="logout_then_login"),
	url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
	url(r'^password_reset/$','django.contrib.auth.views.password_reset',name='password_reset'),
	url(r'^password_reset/done/$','django.contrib.auth.views.password_reset_done',name='password_reset_done'),
	url(r'^password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$','django.contrib.auth.views.password_reset_confirm',name='password_reset_confirm'),
	url(r'^password_reset/complete/$','django.contrib.auth.views.password_reset_complete',name='password_reset_complete'),
	url(r'^register/$', register, name='register'),
	url(r'^dashboard/$', dashboard, name='dashboard'),
	url(r'^edit/$', edit, name='edit'),
	url(r'^users/$', user_list, name='user_list'),
	url(r'^users/follow/$', user_follow, name='user_follow'),
	url(r'^users/(?P<username>[-\w]+)/$', user_detail, name='user_detail'),
	url(r'^edit/location$', add_location, name="add_location"),
]