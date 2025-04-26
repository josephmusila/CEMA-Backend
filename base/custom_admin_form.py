# health_system/admin_forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
import secrets
import string

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Username can only contain letters, digits, and @/./+/-/_',
                code='invalid_username'
            )
        ],
        help_text='Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("CustomUserCreationForm initialized")
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)

    def clean(self):
        print("Running clean method")
        cleaned_data = super().clean()
        print(f"Cleaned data: {cleaned_data}")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(f"Cleaning username: {username}")
        if not username:
            print("Username is empty")
            raise forms.ValidationError('Username is required.')
        if len(username) > 150:
            print("Username too long")
            raise forms.ValidationError('Username must be 150 characters or fewer.')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk if self.instance else None).exists():
            print("Username already taken")
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(f"Cleaning email: {email}")
        if not email:
            print("Email is empty")
            raise forms.ValidationError('Email is required.')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            print("Email already taken")
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        print(f"Entering save method with commit={commit}")
        user = super(forms.ModelForm, self).save(commit=False)
        print(f"Saving user: {user.username}")
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        user.set_password(password)
        print(f"Generated password: {password}")  # Log password for debugging
        
        if commit:
            print("Committing user to database")
            user.save()
            doctor_group, _ = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)
            self.send_password_email(user, password)
        else:
            print("Skipping commit (commit=False)")
            # Temporary workaround: Force commit=True
            print("Forcing commit=True for testing")
            user.save()
            doctor_group, _ = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)
            self.send_password_email(user, password)
        
        print("Exiting save method")
        return user

    def send_password_email(self, user, password):
        from django.core.mail import send_mail
        subject = 'Your Health System Account Password'
        message = f"""
        Hello {user.first_name},

        Your account has been created for the Health System application.
        Below are your login details:

        Username: {user.username}
        Password: {password}
        Email: {user.email}

        Regards,
        CEMA Health System Team
        """
        print(f"Sending email to: {user.email} with password: {password}")
        send_mail(
            subject,
            message,
            'accounts@havenke.com',
            [user.email],
            fail_silently=False,
        )