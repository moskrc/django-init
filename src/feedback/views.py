# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import messages
from django.core.mail.message import EmailMultiAlternatives
from django.shortcuts import render
from django.template import loader
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from forms import ContactForm
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():


            t = loader.get_template('feedback/emails/body.txt')
            c = {
                'data': form.cleaned_data,
                'site': Site.objects.get_current(),
                'date': datetime.now(),
            }

            subject = render_to_string('feedback/emails/subject.txt', c).replace('\n','')
            html_body = t.render(Context(c))
            text_body = strip_tags(html_body)

            msg = EmailMultiAlternatives(subject, text_body, form.cleaned_data['email'], settings.MANAGERS)
            msg.attach_alternative(html_body, "text/html")
            msg.send()

            form = ContactForm()

            messages.success(request, "Ваше сообщение успешно отправлено!")

    else:
        form = ContactForm()

    return render(request, 'feedback/index.html', {'form':form})


        
