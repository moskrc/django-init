# -*- coding: utf-8
from django import template

register = template.Library()

@register.inclusion_tag('accounts/elements/user_video_item.html')
def show_user_video(video_url):
    return {'video_url': video_url}

