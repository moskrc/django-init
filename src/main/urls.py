import flatpages_wysiwyg
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
flatpages_wysiwyg.register()


urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
