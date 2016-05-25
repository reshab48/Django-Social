from django.conf.urls import url, patterns, include

urlpatterns = patterns('images.views',
	url(r'^create/$', 'image_create', name='create'),
	url(r'^detail/ (?P<id>\d+) / (?P<slug>[-\w]+)/$', 'image_detail', name='detail'),
	url(r'^$', 'image_list', name='list'),
	url(r'^like/$', 'image_like', name='like'),
	url(r'^ranking/$', 'image_ranking', name='ranking'),
	url(r'^edit/ (?P<id>\d+) / (?P<slug>[-\w]+)/$', 'image_edit', name='edit'),
)
