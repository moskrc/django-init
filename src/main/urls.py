from django.conf import settings
import flatpages_wysiwyg
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
flatpages_wysiwyg.register()


urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^pages/', include('django.contrib.flatpages.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )