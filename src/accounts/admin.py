from django import forms
from django.contrib import admin
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from registration.models import RegistrationProfile

User = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdmin(UserAdmin):
    fieldsets = (
        (u'Main Info', {'fields': ('username', 'email', 'password', )}),

        (u'Additional Info', {'fields': (
            'first_name',
            'last_name',
            'title',
            'avatar'
        )}),

        (u'Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )}),

        ('Important dates', {'fields': (
            'last_login', 'date_joined'
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'uuid')
    list_filter = ('is_active', 'is_superuser', 'groups', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name',)
    filter_horizontal = ('groups', 'user_permissions',)



admin.site.register(User, UserAdmin)

admin.site.unregister(RegistrationProfile)
