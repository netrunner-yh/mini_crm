from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User, Ticket, Comment


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))


class TicketForm(forms.ModelForm):
    account_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Лицевой счёт'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'ФИО'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Номер телефона'}))
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Загаловок'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Описание'}))

    class Meta:
        model = Ticket
        fields = ['account_number', 'full_name', 'phone_number', 'title', 'description', 'status', 'responsible_person']


class CommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Введите комментарий', 'rows': '3'
    }))

    class Meta:
        model = Comment
        fields = ['content']
