from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField

__all__ = ("UserEditForm",)


UserModel = get_user_model()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
        )
        field_classes = {"username": UsernameField}
