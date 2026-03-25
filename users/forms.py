from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяем Bootstrap-классы к инпутам.
        for field_name in ("username", "email", "password1", "password2"):
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({"class": "form-control"})


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar", "bio", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "first_name" in self.fields:
            self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        if "last_name" in self.fields:
            self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        if "email" in self.fields:
            self.fields["email"].widget.attrs.update({"class": "form-control"})
        if "bio" in self.fields:
            self.fields["bio"].widget.attrs.update({"class": "form-control", "rows": 4})
        if "avatar" in self.fields:
            self.fields["avatar"].widget.attrs.update({"class": "form-control"})
