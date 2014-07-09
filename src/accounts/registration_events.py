# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, user_logged_out
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from registration import signals
#from accounts.forms import EnhancedRegistrationForm
from constance import config


def email_on_activation(user, request, **kwargs):
    """
    Send notification to admin
    """
    c = {
        'site': Site.objects.get_current(),
        'sended': datetime.now(),
        'user': user,
    }

    subject = render_to_string('accounts/email/new_user_subject.txt', c).rstrip('\n')
    html_body = render_to_string('accounts/email/new_user.html', c)
    text_body = strip_tags(html_body)

    msg = EmailMultiAlternatives(subject, text_body, None, config.NEW_USER_EMAIL_TO.split(','))
    msg.attach_alternative(html_body, "text/html")
    msg.send()


signals.user_activated.connect(email_on_activation)


def login_on_activation(user, request, **kwargs):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    messages.add_message(request, messages.INFO, u'Welcome!')
    login(request, user)


signals.user_activated.connect(login_on_activation)


def logout_notifier(sender, request, user, **kwargs):
    messages.info(request, 'You logged out')


user_logged_out.connect(logout_notifier)
