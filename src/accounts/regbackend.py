import hashlib
import random
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.models import Site, RequestSite
from django.core.urlresolvers import reverse
from registration import signals
from registration.backends.simple.views import RegistrationView
from registration.models import RegistrationProfile

from django.db import transaction

from registration.models import RegistrationManager

User = get_user_model()


class CustomRegistrationManager(RegistrationManager):
    def create_inactive_user(self, email, password, site, send_email=True, **kwargs):
        new_user = User.objects.create_user(email, email, password, site, **kwargs)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user

    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile(self, user):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        email = user.email
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        activation_key = hashlib.sha1(salt + email).hexdigest()
        return self.create(user=user, activation_key=activation_key)


class CustomRegistrationProfile(RegistrationProfile):
    class Meta:
        proxy = True

    objects = CustomRegistrationManager()


class CustomRegistrationView(RegistrationView):
    def register(self, request, **cleaned_data):
        first_name, last_name, email, password, nickname = cleaned_data['first_name'], \
                                                 cleaned_data['last_name'] or '', \
                                                 cleaned_data['email'], \
                                                 cleaned_data['password'],\
                                                 cleaned_data['email']


        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = User.objects.create_user(nickname, email, password, site,
                                                                          **{'first_name': first_name,
                                                                             'last_name': last_name,
                                                                             })

        new_user = authenticate(username=nickname, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_success_url(self, request, user):
        return reverse('home')




# class CustomActivationView(ActivationView):
#     def activate(self, request, activation_key):
#         return RegistrationProfile.objects.activate_user(activation_key)
#
#
#     def get_success_url(self, request, user):
#         return ('index', (), {})
