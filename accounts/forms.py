from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import UserProfile


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("User does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("No longer Active")
        return super(UserLoginForm, self).clean()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email2 = forms.EmailField(label='Confirm Email')
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    # def clean(self):            # Non Field error. Shows as a general error but can be used
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get('email2')
    #     if email2 != email:
    #         raise forms.ValidationError("Emails Don't match")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("Email already taken")
    #
    #     return super(UserRegistrationForm, self).clean()

    def clean_email2(self):     # Field Errors. Naming and ordering does matter see cleaned methods.
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email2 != email:
            raise forms.ValidationError("Emails Don't match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email already taken")
        return email


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = [
#             'friend_request',
#             'friends_list'
#         ]