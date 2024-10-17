from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.core.exceptions import ValidationError
from .models import Todo  

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'deadline', 'urgency', 'importance',]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  
        }

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['username', 'age', 'email', 'password']
    
    def save(self, commit=True):  
        user = super().save(commit=False)  
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password']) 
        if commit:  
            user.save()
        return user
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 4:
            raise forms.ValidationError("パスワードは4文字以上である必要があります。")

        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e)

        return password

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

