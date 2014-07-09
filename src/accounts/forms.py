# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class EnhancedRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(render_value=False), label=u"Password",
                               min_length=3)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(EnhancedRegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                "This email address is already in use. Please supply a different email address.")
        return self.cleaned_data['email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class UserProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', )


