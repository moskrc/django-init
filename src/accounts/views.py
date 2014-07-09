# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from forms import UserProfileForm


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, u'Profile was successfully updated')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form, 'user': request.user,})


def ext_profile(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    return render(request, 'accounts/ext_profile.html', {'user': user})
