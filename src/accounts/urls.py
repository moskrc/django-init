
from django.conf.urls import *
from django.contrib.auth.views import logout, login
from django.core.urlresolvers import reverse_lazy

from forms import EnhancedRegistrationForm
from regbackend import CustomRegistrationProfile, CustomRegistrationView
from registration.backends.default.views import RegistrationView


urlpatterns = patterns('accounts.views',
    url(r'^profile/$', 'profile', name='accounts_profile'),
)

urlpatterns += patterns('',
    url(r'^register/$', CustomRegistrationView.as_view(form_class=EnhancedRegistrationForm),  name="register"),
    url(r'^login/$', login, {'extra_context':{'registration_form':EnhancedRegistrationForm()}}, name='auth_login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('home')}, name='auth_logout'),
    #url(r'^activate/(?P<activation_key>\w+)/$', CustomActivationView.as_view(), name='registration_activate'),


    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done')
)

urlpatterns += patterns('accounts.views',
    url(r'^(?P<user_id>\d+)/$', 'ext_profile', name='accounts_ext_profile'),
)
