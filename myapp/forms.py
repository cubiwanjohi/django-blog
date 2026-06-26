from django import forms
from .models import Comment


# ──────────────────────────────
# COMMENT FORM
# ──────────────────────────────
class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['body', 'guest_name', 'guest_email', 'parent']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment...',
                'class': 'form-control',
            }),
            'guest_name': forms.TextInput(attrs={
                'placeholder': 'Your name *',
                'class': 'form-control',
            }),
            'guest_email': forms.EmailInput(attrs={
                'placeholder': 'Email (optional)',
                'class': 'form-control',
            }),
            # Hidden field — set programmatically for replies
            'parent': forms.HiddenInput(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # If user is logged in, hide guest fields — they don't need them
        if user and user.is_authenticated:
            self.fields.pop('guest_name')
            self.fields.pop('guest_email')

    def clean(self):
        cleaned_data = super().clean()
        guest_name = cleaned_data.get('guest_name')
        # guest_name field may not exist if user is logged in
        if 'guest_name' in self.fields and not guest_name:
            raise forms.ValidationError("Please provide your name.")
        return cleaned_data


# ──────────────────────────────
# SEARCH FORM
# ──────────────────────────────
class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts...',
            'class': 'form-control',
            'autofocus': True,
        })
    )

    def clean_q(self):
        query = self.cleaned_data.get('q', '').strip()
        if query and len(query) < 3:
            raise forms.ValidationError("Search query must be at least 3 characters.")
        return query


# ──────────────────────────────
# REGISTER FORM
# ──────────────────────────────
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control',
        })
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS class and placeholder to all fields
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'form-control',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
            'class': 'form-control',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Prevent duplicate email addresses
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email