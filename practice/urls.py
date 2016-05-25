from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^account/', include('account.urls')),
    (r'^images/', include('images.urls', namespace='images')),
    ('social-auth/', include('social.apps.django_app.urls', namespace='social')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
