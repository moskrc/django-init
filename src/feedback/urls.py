from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'feedback.views.index', name='feedback_index'),
)
