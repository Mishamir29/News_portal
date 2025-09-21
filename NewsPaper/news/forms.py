from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Post, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # или SelectMultiple
        required=True
    )

    class Meta:
        model = Post
        fields = {'author','title', 'content', 'categories'}


# class BasicSignupForm(SignupForm):
#
#     def save(self, request):
#         user = super(BasicSignupForm, self).save(request)
#         basic_group = Group.objects.get(name='common')
#         basic_group.user_set.add(user)
#         return user


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        email = forms.EmailField()

        class Meta:
            model = User
            fields = ('username', 'email', 'password1', 'password2')


class MyCustomSignupForm(SignupForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ' '
        self.fields['username'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self,request):
        user = super().save(request)
        list(messages.get_messages(request))
        messages.success(request, "Вы успешно зарегистрировались.\n Добро пожаловать на 'Новостной портал'")
        return user